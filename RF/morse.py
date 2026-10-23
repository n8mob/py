"""morse — generate and play Morse code tones using only the standard library.

Quick start:

    import morse
    morse.play("SOS")                      # play through the speakers
    morse.encode("Hello")                  # '.... . .-.. .-.. ---'
    morse.decode(".... ..")                # 'HI'
    morse.save_wav("CQ CQ", "cq.wav")      # write a WAV file

Timing follows the PARIS standard: one "unit" lasts 1.2 / wpm seconds.
A dot is 1 unit, a dash 3, the gap inside a character 1, between
characters 3, and between words 7. Passing ``farnsworth_wpm`` stretches
the gaps between characters and words while keeping the characters
themselves at full speed, which is the usual way to learn.

Command line:

    python morse.py "SOS" --wpm 20 --freq 700
    python morse.py "SOS" --out sos.wav
"""

from __future__ import annotations

import io
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.parse
import wave
import xml.etree.ElementTree as ET

__all__ = ["MORSE_CODE", "encode", "decode", "generate", "to_wav_bytes",
           "save_wav", "play", "play_feed"]

MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.", "!": "-.-.--",
    "/": "-..-.", "(": "-.--.", ")": "-.--.-", "&": ".-...", ":": "---...",
    ";": "-.-.-.", "=": "-...-", "+": ".-.-.", "-": "-....-", "_": "..--.-",
    '"': ".-..-.", "$": "...-..-", "@": ".--.-.",
}
_REVERSE = {code: char for char, code in MORSE_CODE.items()}

DEFAULT_WPM = 15

SAMPLE_RATE = 44100


def encode(text: str, *, strict: bool = False) -> str:
    """Convert text to Morse. Letters are separated by spaces, words by ' / '.

    Characters with no Morse equivalent are skipped, or raise ValueError
    when ``strict`` is true.
    """
    words = []
    for word in text.upper().split():
        letters = []
        for ch in word:
            if ch in MORSE_CODE:
                letters.append(MORSE_CODE[ch])
            elif strict:
                raise ValueError(f"No Morse code for {ch!r}")
        if letters:
            words.append(" ".join(letters))
    return " / ".join(words)


def decode(code: str) -> str:
    """Convert Morse (letters split by spaces, words by '/') back to text.

    Unknown sequences become '?'.
    """
    words = []
    for word in code.strip().split("/"):
        letters = [_REVERSE.get(sym, "?") for sym in word.split()]
        if letters:
            words.append("".join(letters))
    return " ".join(words)


def _timeline(code: str, wpm: float, farnsworth_wpm: float | None):
    """Yield (is_tone, seconds) pairs for a Morse string."""
    unit = 1.2 / wpm
    # Farnsworth: stretch the inter-character and inter-word gaps only.
    if farnsworth_wpm and farnsworth_wpm < wpm:
        gap_unit = (60 / farnsworth_wpm - 31 * unit) / 19
    else:
        gap_unit = unit

    words = [w.split() for w in code.strip().split("/") if w.split()]
    for wi, letters in enumerate(words):
        if wi:
            yield False, 7 * gap_unit
        for li, letter in enumerate(letters):
            if li:
                yield False, 3 * gap_unit
            for si, sym in enumerate(letter):
                if si:
                    yield False, unit
                if sym == ".":
                    yield True, unit
                elif sym == "-":
                    yield True, 3 * unit
                else:
                    raise ValueError(f"Invalid Morse symbol {sym!r}")


def generate(text: str, *, wpm: float = DEFAULT_WPM, freq: float = 600,
             volume: float = 0.5, farnsworth_wpm: float | None = None,
             sample_rate: int = SAMPLE_RATE, is_code: bool = False) -> bytes:
    """Return 16-bit mono PCM samples for ``text``.

    Set ``is_code=True`` to pass a ready-made Morse string ('... --- ...')
    instead of plain text. Each tone gets a short fade in and out so it
    doesn't click.
    """
    if wpm <= 0:
        raise ValueError("wpm must be positive")
    code = text if is_code else encode(text)
    amp = max(0.0, min(1.0, volume)) * 32767
    ramp = int(sample_rate * 0.005)  # 5 ms
    step = 2 * math.pi * freq / sample_rate

    out = bytearray()
    for is_tone, seconds in _timeline(code, wpm, farnsworth_wpm):
        n = int(round(seconds * sample_rate))
        if not is_tone:
            out += bytes(2 * n)
            continue
        r = min(ramp, n // 2)
        samples = []
        for i in range(n):
            env = 1.0
            if i < r:
                env = i / r
            elif i >= n - r:
                env = (n - 1 - i) / r
            samples.append(int(amp * env * math.sin(step * i)))
        out += struct.pack(f"<{n}h", *samples)
    # Trailing silence so players don't cut off the last tone.
    out += bytes(2 * int(sample_rate * 0.1))
    return bytes(out)


def to_wav_bytes(pcm: bytes, sample_rate: int = SAMPLE_RATE) -> bytes:
    """Wrap raw 16-bit mono PCM in a WAV container."""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm)
    return buf.getvalue()


def save_wav(text: str, path: str, **kwargs) -> str:
    """Write ``text`` as Morse audio to a WAV file. Takes the same options as generate()."""
    rate = kwargs.get("sample_rate", SAMPLE_RATE)
    with open(path, "wb") as f:
        f.write(to_wav_bytes(generate(text, **kwargs), rate))
    return path


def _play_wav_file(path: str) -> None:
    try:
        import sound # pythonista
    except ImportError:
        sound = None
    if sound is not None:
        player = sound.Player(path)
        player.play()
        time.sleep(player.duration + 0.1) # prevent premature close of player
        return

    if sys.platform == "win32":
        import winsound
        winsound.PlaySound(path, winsound.SND_FILENAME)
        return

    if sys.platform == "darwin":
        players = [["afplay"]]

    else:
        players = [["paplay"], ["pw-play"], ["aplay", "-q"],
                   ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]]

    for cmd in players:
        if shutil.which(cmd[0]):
            subprocess.run(cmd + [path], check=True)
            return
    raise RuntimeError("No audio player found (tried: "
                       + ", ".join(c[0] for c in players) + ")")


def play(text: str, **kwargs) -> None:
    """Play ``text`` as Morse through the speakers. Blocks until done.

    Takes the same options as generate(). Uses winsound on Windows, afplay
    on macOS, and paplay / pw-play / aplay / ffplay on Linux.
    """
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        save_wav(text, path, **kwargs)
        _play_wav_file(path)
    finally:
        os.remove(path)


def play_feed(url: str, wpm: float = DEFAULT_WPM):
    with urllib.request.urlopen(url) as resp:
        root = ET.parse(resp).getroot()

    for item in root.iter("item"):
        title = item.findtext("title")
        DEBUG = True
        if DEBUG:
            print(title)
        play(title, wpm=wpm)
        time.sleep(0.4)
        play("=", wpm=wpm)
        time.sleep(0.8)


def _main(argv=None) -> None:
    import argparse
    p = argparse.ArgumentParser(description="Play text as Morse code.")
    p.add_argument("text", help="text to send (or Morse with --code)")
    p.add_argument("--wpm", type=float, default=DEFAULT_WPM, help=f"speed in words per minute (default {DEFAULT_WPM})")
    p.add_argument("--farnsworth", type=float, metavar="WPM", help="effective speed for spacing")
    p.add_argument("--freq", type=float, default=600, help="tone frequency in Hz (default 600)")
    p.add_argument("--volume", type=float, default=0.5, help="0.0 to 1.0 (default 0.5)")
    p.add_argument("--code", action="store_true", help="input is already Morse")
    p.add_argument("--out", metavar="FILE", help="write a WAV file instead of playing")
    a = p.parse_args(argv)

    opts = dict(wpm=a.wpm, freq=a.freq, volume=a.volume,
                farnsworth_wpm=a.farnsworth, is_code=a.code)

    url = urllib.parse.urlparse(a.text)
    if url.scheme in ("https", "http") and url.netloc:
        print(f'Getting feed from: {a.text}')
        play_feed(a.text, a.wpm)
        return
             
    print(a.text if a.code else encode(a.text))
    if a.out:
        save_wav(a.text, a.out, **opts)
        print(f"Wrote {a.out}")
    else:
        play(a.text, **opts)


if __name__ == "__main__":
    _main()
