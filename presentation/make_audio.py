#!/usr/bin/env python3
"""Narrate LISTEN.md to WAV with Piper — fully offline, nothing leaves the machine.

One file per track so a track can be re-listened to on its own, plus a single combined file.
Markdown is stripped to speech: emphasis markers and headings are removed rather than read out,
and a short silence is inserted at paragraph breaks so it does not sound like one long run-on.

    <venv>/bin/python make_audio.py <model.onnx> <out_dir>
"""
import os
import re
import struct
import sys
import wave

from piper import PiperVoice
from piper.config import SynthesisConfig

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "LISTEN.md")


def speechify(md):
    """Markdown -> what a narrator should actually say."""
    md = re.sub(r"^\*.*?written to be heard.*?\*$", "", md, flags=re.M | re.I)
    md = re.sub(r"(?s)\*\*To turn this into audio:\*\*.*?(?=\n---)", "", md)
    md = re.sub(r"`([^`]*)`", r"\1", md)
    md = re.sub(r"\*\*([^*]*)\*\*", r"\1", md)
    md = re.sub(r"\*([^*]*)\*", r"\1", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    md = md.replace("—", ", ").replace("–", "-")
    return md


def tracks(md):
    """Split on the track headings; the H1 preamble is dropped."""
    parts = re.split(r"(?m)^## (Track \d+[^\n]*)$", md)
    out = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1].replace("---", " ").strip()
        body = re.sub(r"\n{2,}", "\n\n", body)
        out.append((title, f"{title}.\n\n{body}"))
    return out


def silence(n_frames, rate):
    return struct.pack("<h", 0) * int(rate * n_frames)


def main(model, outdir):
    voice = PiperVoice.load(model)
    cfg = SynthesisConfig(length_scale=1.06)      # a touch slower than default: this is study audio
    rate = voice.config.sample_rate
    os.makedirs(outdir, exist_ok=True)

    md = speechify(open(SRC).read())
    combined = []
    for idx, (title, text) in enumerate(tracks(md), 1):
        path = os.path.join(outdir, f"{idx:02d}-{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:40]}.wav")
        with wave.open(path, "wb") as w:
            voice.synthesize_wav(text, w, syn_config=cfg)
        with wave.open(path, "rb") as w:
            combined.append(w.readframes(w.getnframes()))
        combined.append(silence(0.9, rate))
        print(f"  {idx:02d}  {os.path.getsize(path)/1048576:5.1f} MB  {title}")

    full = os.path.join(outdir, "00-FULL-listen.wav")
    with wave.open(full, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"".join(combined))
    secs = os.path.getsize(full) / (rate * 2)
    print(f"\n  combined -> {full}\n  {secs/60:.1f} minutes · {os.path.getsize(full)/1048576:.0f} MB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
