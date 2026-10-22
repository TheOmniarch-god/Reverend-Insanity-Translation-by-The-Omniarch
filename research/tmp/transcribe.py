import av, numpy as np
from faster_whisper import WhisperModel
c = av.open("tmp/test_v3.mp3")
st = c.streams.audio[0]
rs = av.AudioResampler(format="flt", layout="mono", rate=16000)
chunks=[]
for fr in c.decode(st):
    for r in rs.resample(fr):
        chunks.append(r.to_ndarray().reshape(-1))
audio = np.concatenate(chunks).astype(np.float32)
print("samples", len(audio)/16000, flush=True)
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, info = m.transcribe(audio, language="en", beam_size=5, vad_filter=True)
print("duration", info.duration, flush=True)
with open("tmp/segments.txt","w") as f:
    for s in segs:
        f.write(f"{s.start:.2f}\t{s.end:.2f}\t{s.text.strip()}\n")
print("done", flush=True)
