from pathlib import Path
import math, random, wave, json, hashlib

ROOT = Path('/Users/leoguinan/future-radio-sound-cues')
CUES = ROOT / 'cues'
SR = 48000
SEED = 120026
rng = random.Random(SEED)

def write(name, samples):
    path = CUES / name
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        frames = bytearray()
        for x in samples:
            x = max(-1.0, min(1.0, x))
            frames += int(x * 32767).to_bytes(2, 'little', signed=True)
        w.writeframes(frames)
    return path

def env(t, dur, attack=.02, release=.08):
    return min(1, t/attack) * min(1, (dur-t)/release) if 0 <= t <= dur else 0

def sine(dur, fn, amp=.3):
    n = int(SR*dur)
    return [amp*math.sin(2*math.pi*fn*(i/SR))*env(i/SR,dur) for i in range(n)]

def add(*tracks):
    n=max(map(len,tracks)); out=[0.0]*n
    for tr in tracks:
        for i,x in enumerate(tr): out[i]+=x
    return out

def click(t, dur, amp=.7):
    n=int(SR*dur); start=int(SR*t)
    out=[0.0]*(start+n)
    for i in range(n): out[start+i]=amp*math.exp(-i/(SR*.012))*rng.uniform(-1,1)
    return out

def tone_at(t0, dur, freq, amp=.3, harmonics=1):
    n=int(SR*(t0+dur))+1; out=[0.0]*n
    for i in range(int(SR*dur)):
        t=i/SR; e=env(t,dur,.03,.15)
        val=sum(math.sin(2*math.pi*freq*h*t)/(h**1.3) for h in range(1,harmonics+1))
        out[int(SR*t0)+i]=amp*e*val
    return out

def noise(dur, amp=.05): return [rng.uniform(-amp,amp)*env(i/SR,dur,.05,.2) for i in range(int(SR*dur))]

# FR-CARRIER: narrow steady station tone with quiet air, connection only.
dur=4.0
carrier=add(sine(dur,440,.23), noise(dur,.018))
write('fr-carrier.wav', carrier)

# FR-PACKET and identical foreground stems: 4 bars at 96 BPM, deterministic seed.
dur=10.0
agn=[0.0]*int(SR*dur); bor=[0.0]*int(SR*dur); leo=[0.0]*int(SR*dur)
# Agnolo: dry strikes and an intentionally empty downbeat.
for t in [0.0,1.25,2.5,3.75,5.0,6.25,7.5,8.75]:
    c=click(t,.16,.62)
    for i,x in enumerate(c):
        if i<len(agn): agn[i]+=x
# Borges: unfinished two-note figure returning in another register.
for t,f in [(0.3,196),(1.0,233),(2.8,196),(3.5,277),(5.3,196),(6.0,233),(7.8,196),(8.5,277)]:
    tr=tone_at(t,.55,f,.14,3)
    for i,x in enumerate(tr):
        if i<len(bor): bor[i]+=x
# Leonardo: ascending breath phrase, last note unresolved.
for base in [0.15,2.65,5.15,7.65]:
    for j,f in enumerate([330,392,466]):
        tr=tone_at(base+j*.22,.34,f,.10,2)
        for i,x in enumerate(tr):
            if i<len(leo): leo[i]+=x
write('fr-agnolo-isolation.wav',agn)
write('fr-borges-isolation.wav',bor)
write('fr-leonardo-isolation.wav',leo)
write('fr-packet.wav',add(agn,bor,leo))

# FR-RECORD: returning bowed note with one extra overtone.
write('fr-record.wav', add(tone_at(0,.9,220,.22,2), tone_at(.18,.72,330,.09,3)))
# FR-OPEN: rising woodwind-like partials, suspended ending.
open_tr=[]
for t,f in [(0,330),(.35,392),(.7,440),(1.05,523)]: open_tr.append(tone_at(t,.65,f,.11,2))
write('fr-open.wav',add(*open_tr))
# FR-EVAL: pencil-like dry click followed by a precisely timed soft tone.
eval_tr=click(0,.12,.45)
eval_tr=add(eval_tr,tone_at(.22,.55,660,.12,2))
write('fr-eval.wav',eval_tr)
# FR-ASSEMBLE: edit clicks and a short station bed, not a release signal.
asm=add(click(0,.08,.3),click(.32,.08,.3),click(.64,.08,.3),sine(1.2,440,.08))
write('fr-assemble.wav',asm)

manifest={'cue_set':'Future Radio Sound Bible v1','generator':'deterministic Python synthesis','seed':SEED,'sample_rate':SR,'status':'prototype','cues':[],'residuals':['These are symbolic cue prototypes, not a finished score or claim about meaning.','No cue implies consent, publication, funding, achievement, or authorization.']}
for p in sorted(CUES.glob('*.wav')):
    with wave.open(str(p),'rb') as w: frames=w.getnframes(); rate=w.getframerate()
    manifest['cues'].append({'file':str(p.relative_to(ROOT)),'duration_sec':frames/rate,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ROOT/'manifests/cue-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'files':len(manifest['cues']),'sample_rate':SR,'seed':SEED},indent=2))
