# Narration production

The course includes 160 independently playable recordings: 90 main pages, 60 decision feedback clips and ten recall-answer clips. Ten continuous chapter tracks provide a separate listening format. All text is specific to this course; the social course recordings are not reused. Builds use the committed AAC files. Visual-only edits do not require speech regeneration.

Voice: pinned Kokoro-82M v1.0 ONNX CPU, `af_heart`, speed 1.0. Paragraph boundaries use explicit 0.65-second pauses. Recall and transfer prompts add a longer beat. The separately obtained record-demo skill verifies model and voice hashes before synthesis. Its implementation is referenced, not bundled.

Canonical visible content is in `course.json`. Run `python3 scripts/sync_sources.py` to prepare changed recording scripts, or `--check` to detect drift. Speech-specific pronunciation is stored separately in each scene’s `say` field. The transcript strips phoneme and pause markup.

To regenerate all speech with the separately obtained skill:

```sh
uv run /path/to/record-demo/scripts/tts.py "$PWD/production/af-heart" af_heart 1.0
uv run /path/to/record-demo/scripts/phonemes.py "$PWD/production/af-heart" --all
uv run scripts/screen_narration.py
python3 production/encode_audio.py
```

The encoder requires FFmpeg and the completed raw WAV files; raw WAVs and model assets are ignored by Git. It writes 48 kHz mono AAC at 160 kbps, normalized to -16 LUFS and -1.5 dBTP. Chapter listening tracks include deliberate gaps before suggested answers.

`qa/narration-asr.json` records independent transcription screening and identifies the model per clip. Flagged clips and a sample across chapters receive additional small.en checks. `qa/narration-phonemes.txt` records the actual speech tokenizer’s output. These checks do not constitute human listening approval, a guarantee of pronunciation or a learner pilot. Current model/voice provenance and encoded clip hashes are in `audio/manifest.json`.
