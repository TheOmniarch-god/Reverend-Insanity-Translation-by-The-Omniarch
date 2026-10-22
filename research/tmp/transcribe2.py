import av, numpy as np, json
from faster_whisper import WhisperModel
c = av.open("tmp/test_v3.mp3"); st = c.streams.audio[0]
rs = av.AudioResampler(format="flt", layout="mono", rate=16000)
audio = np.concatenate([r.to_ndarray().reshape(-1) for fr in c.decode(st) for r in rs.resample(fr)]).astype(np.float32)
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, info = m.transcribe(audio, language="en", beam_size=5, vad_filter=True, word_timestamps=True)
words=[]
for s in segs:
    for w in s.words:
        words.append({"w":w.word.strip(),"s":w.start,"e":w.end})
json.dump(words, open("tmp/words.json","w"))
print("done", len(words), flush=True)
