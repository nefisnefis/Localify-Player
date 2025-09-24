"""
Local Spotify-style music server with volume control + shuffle/repeat buttons.
Requires: pip install flask mutagen Pillow
"""
from flask import Flask, request, render_template_string, send_file, redirect, url_for, Response, abort
from pathlib import Path
from werkzeug.utils import secure_filename
from mutagen import File as MutagenFile
from PIL import Image
import io, os, base64
from pypresence import Presence
import time

app = Flask(__name__)
DISCORD_CLIENT_ID = "1420442354120396821"  # ID twojej aplikacji
RPC = Presence(DISCORD_CLIENT_ID)
try:
    RPC.connect()
except Exception as e:
    print("Nie udało się połączyć z Discord RPC:", e)

MUSIC_DIR = Path.cwd() / 'music'
MUSIC_DIR.mkdir(exist_ok=True)
ALLOWED_EXT = {'.mp3', '.m4a', '.wav', '.flac', '.ogg'}
CHUNK_SIZE = 1024 * 32

def allowed_file(filename): return Path(filename).suffix.lower() in ALLOWED_EXT

def extract_metadata(path: Path):
    meta = {'title': path.stem, 'artist': 'Unknown', 'album': '', 'cover': None}
    try:
        audio = MutagenFile(path)
        if audio is None: return meta
        tags = audio.tags or {}
        for k,v in tags.items():
            k_lower = str(k).lower()
            val = v[0] if isinstance(v,list) else v
            if 'title' in k_lower or k_lower=='©nam':
                meta['title']=str(val)
            if 'artist' in k_lower or k_lower=='tpe1' or k_lower=='©art':
                meta['artist']=str(val)
            if 'album' in k_lower or k_lower=='talb' or k_lower=='©alb':
                meta['album']=str(val)
        for k in tags.keys():
            if k.startswith('APIC') or k.startswith('covr'):
                pic = tags[k].data if hasattr(tags[k],'data') else tags[k][0]
                im = Image.open(io.BytesIO(bytes(pic)))
                im.thumbnail((400,400))
                buf = io.BytesIO()
                im.save(buf,format='PNG')
                meta['cover']='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
                break
    except Exception: pass
    return meta

def list_tracks():
    files=[]
    for i,p in enumerate(sorted(MUSIC_DIR.iterdir())):
        if p.is_file() and allowed_file(p.name):
            meta=extract_metadata(p)
            files.append({'path':str(p.resolve()),'meta':meta})
    return files

def partial_response(path):
    file_size=os.path.getsize(path)
    range_header=request.headers.get('Range')
    if not range_header: return send_file(path,conditional=True)
    bytes_unit,bytes_range=range_header.split('=')
    start_str,end_str=bytes_range.split('-')
    start=int(start_str) if start_str else 0
    end=int(end_str) if end_str else file_size-1
    length=end-start+1
    def generate():
        with open(path,'rb') as f:
            f.seek(start)
            bytes_remaining=length
            while bytes_remaining>0:
                chunk=f.read(min(CHUNK_SIZE,bytes_remaining))
                if not chunk: break
                bytes_remaining-=len(chunk)
                yield chunk
    rv=Response(generate(),status=206,mimetype='audio/mpeg')
    rv.headers.add('Content-Range',f'bytes {start}-{end}/{file_size}')
    rv.headers.add('Accept-Ranges','bytes')
    rv.headers.add('Content-Length',str(length))
    return rv

HTML="""
<!doctype html><html lang="pl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Localify Player</title>
<style>
body{margin:0;font-family:sans-serif;background:#121212;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;height:100vh}
header{padding:10px;text-align:center}
#cover{width:300px;height:300px;object-fit:cover;border-radius:10px;margin-top:20px}
#title{font-size:1.4em;margin-top:15px}
#artist{font-size:1em;color:#bbb}
.controls{display:flex;align-items:center;gap:20px;margin-top:20px;flex-wrap:wrap;justify-content:center}
button{background:none;border:none;color:#fff;font-size:2em;cursor:pointer}
#progressContainer{width:80%;margin-top:15px}
#progress{width:100%}
#volume{width:100px}
.tracklist{margin-top:30px;width:90%;max-width:600px;overflow-y:auto}
.trackitem{padding:8px;cursor:pointer;border-bottom:1px solid #333}
.trackitem:hover{background:#1f1f1f}
</style>
</head><body>
<header><h2>🎵 Localify Player</h2></header>
<img id="cover" src="https://via.placeholder.com/300x300.png?text=No+Cover">
<div id="title">—</div>
<div id="artist">—</div>
<div class="controls">
<button id="prevBtn">⏮️</button>
<button id="playBtn">▶️</button>
<button id="nextBtn">⏭️</button>
<button id="shuffleBtn">🔀</button>
<button id="repeatBtn">🔁</button>
<input type="range" id="volume" min="0" max="1" step="0.01" value="1">
</div>
<div id="progressContainer">
<input type="range" id="progress" value="0" min="0" max="100">
</div>
<div class="tracklist">
{% for t in tracks %}
<div class="trackitem" data-index="{{ loop.index0 }}" data-stream="/stream/{{ loop.index0 }}" data-title="{{t.meta.title}}" data-artist="{{t.meta.artist}}" data-cover="{{t.meta.cover if t.meta.cover else ''}}">
{{t.meta.title}} — <span style="color:#888">{{t.meta.artist}}</span>
</div>
{% endfor %}
</div>
<audio id="player"></audio>
<script>
let tracks=[];
document.querySelectorAll('.trackitem').forEach(e=>{
 tracks.push({
   stream:e.dataset.stream,
   title:e.dataset.title,
   artist:e.dataset.artist,
   cover:e.dataset.cover
 });
});
let currentIndex=0;
let shuffle=false,repeat=false;
const player=document.getElementById('player');
const cover=document.getElementById('cover');
const title=document.getElementById('title');
const artist=document.getElementById('artist');
const playBtn=document.getElementById('playBtn');
const prevBtn=document.getElementById('prevBtn');
const nextBtn=document.getElementById('nextBtn');
const shuffleBtn=document.getElementById('shuffleBtn');
const repeatBtn=document.getElementById('repeatBtn');
const volume=document.getElementById('volume');
const progress=document.getElementById('progress');

function loadTrack(i){
  if(i<0) i=tracks.length-1; if(i>=tracks.length) i=0;
  currentIndex=i;
  player.src=tracks[i].stream;
  cover.src=tracks[i].cover || 'https://via.placeholder.com/300x300.png?text=No+Cover';
  title.textContent=tracks[i].title;
  artist.textContent=tracks[i].artist;
  player.play();
  playBtn.textContent='⏸️';

  // ⇩⇩⇩ wysyłamy RPC do Discorda ⇩⇩⇩
  fetch('/rpc', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({title: tracks[i].title, artist: tracks[i].artist})
  });
}
playBtn.addEventListener('click',()=>{
 if(player.paused){player.play();playBtn.textContent='⏸️';}
 else {player.pause();playBtn.textContent='▶️';}
});
prevBtn.addEventListener('click',()=>loadTrack(currentIndex-1));
nextBtn.addEventListener('click',()=>loadTrack(currentIndex+1));
player.addEventListener('ended',()=>{
 if(repeat){
   player.currentTime=0; player.play();
 }else if(shuffle){
   loadTrack(Math.floor(Math.random()*tracks.length));
 }else{
   loadTrack(currentIndex+1);
 }
});
player.addEventListener('timeupdate',()=>{
 if(player.duration){
   progress.value=(player.currentTime/player.duration)*100;
 }
});
progress.addEventListener('input',()=>{
 if(player.duration){
   player.currentTime=(progress.value/100)*player.duration;
 }
});
volume.addEventListener('input',()=>{
 player.volume=volume.value;
});
shuffleBtn.addEventListener('click',()=>{
 shuffle=!shuffle;
 shuffleBtn.style.color=shuffle?'#1db954':'#fff';
});
repeatBtn.addEventListener('click',()=>{
 repeat=!repeat;
 repeatBtn.style.color=repeat?'#1db954':'#fff';
});
document.querySelectorAll('.trackitem').forEach((e,i)=>{
 e.addEventListener('click',()=>loadTrack(i));
});
if(tracks.length>0)loadTrack(0);
</script>
</body></html>
"""

@app.route('/')
def index():
    tracks=list_tracks()
    return render_template_string(HTML,tracks=tracks)

@app.route('/upload',methods=['POST'])
def upload():
    if 'file' not in request.files: return 'Brak pliku',400
    f=request.files['file']
    if f.filename=='':return 'Pusta nazwa pliku',400
    filename=secure_filename(f.filename)
    if not allowed_file(filename):return 'Nieobsługiwane rozszerzenie',400
    path=MUSIC_DIR/filename
    i=1
    while path.exists():
        path=MUSIC_DIR/f"{Path(filename).stem}_{i}{Path(filename).suffix}"
        i+=1
    f.save(path)
    return redirect(url_for('index'))

@app.route('/stream/<int:track_id>')
def stream(track_id):
    tracks=list_tracks()
    if track_id<0 or track_id>=len(tracks):abort(404)
    return partial_response(tracks[track_id]['path'])

@app.route('/download/<int:track_id>')
def download(track_id):
    tracks=list_tracks()
    if track_id<0 or track_id>=len(tracks):abort(404)
    return send_file(tracks[track_id]['path'],as_attachment=True)
@app.route('/rpc', methods=['POST'])
def rpc():
    data = request.get_json(force=True)
    title = data.get('title', 'Unknown')
    artist = data.get('artist', 'Unknown')
    try:
        RPC.update(state=f"by {artist}", details=title, large_image="logo.png")
    except Exception as e:
        print("Błąd RPC:", e)
    return jsonify({'ok': True})

if __name__=='__main__':
    print("Open on phone: http://<YOUR_IP>:5000")
    app.run(host='0.0.0.0',port=5000,debug=True)

