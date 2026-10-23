import math
import os
import subprocess
import sys
import wave
import struct

_tone_v = [697, 770, 852, 941]
_tone_h = [1209, 1336, 1477, 1633]
_alt_nums = {'*': 'star', '#': 'pound', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}
_num_tones = {
    '1': (0, 0), '2': (0, 1), '3': (0, 2), 'A': (0, 3),
    '4': (1, 0), '5': (1, 1), '6': (1, 2), 'B': (1, 3),
    '7': (2, 0), '8': (2, 1), '9': (2, 2), 'C': (2, 3),
    'star': (3, 0), '0': (3, 1), 'pound': (3, 2), 'D': (3, 3)
}

nums = {}

def toner(v,h):
    return _tone_v[v], _tone_h[h]

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

def play(filename):
    subprocess.run(['afplay', filename])


def tone_name(n):
    n_str = str(n)
    if n_str in _num_tones:
        return n_str
    else:
        return _alt_nums[n_str]


def blue_box(n, duration=0.5):
    nname = tone_name(n)
    if n in nums:
        del nums[n]
    if nname not in nums:
        filename = f'tone_{nname}.wav'
        if os.path.exists(filename):
            nums[nname] = filename
        else:
            generate_tone(filename, toner(*_num_tones[tone_name(n)]), duration)
            nums[nname] = filename

    play(nums[nname])


def play_sequence(sequence, duration=0.5):
    for n in sequence:
        nname = tone_name(n)
        print(f'tone: {n} ({nname})')
        blue_box(nname, duration)


if __name__ == '__main__':
    play_sequence('d1#', duration=0.3)
