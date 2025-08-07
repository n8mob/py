import math
import subprocess
import wave
import struct

def generate_tone(filename, freqs, duration=0.5, samplerate=44100):
    frames = []
    for i in range(int(duration * samplerate)):
        t = i / samplerate
        sample = sum(math.sin(2*math.pi * f * t) for f in freqs)
        sample = int(sample / len(freqs) * 32767)
        frames.append(struct.pack("<h", sample))

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(b''.join(frames))

    subprocess.run(['afplay', filename])


