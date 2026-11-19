# Common Ground: Personality psychology

An original introductory personality psychology course using fictional repair-café stories, independently narrated lessons, decisions, written transfer, retrieval and field practice.

Live: https://snowch.github.io/common-ground-personality-psychology/

Ten chapters · 90 learner-paced pages · 40 concept figures · 20 decisions · 160 recordings. The study and visual companions collect research and diagrams. Offline saves the whole course in the browser; external research sites require a connection. Playback shows elapsed and remaining time at the selected speed.

## Build

```sh
python3 build.py
python3 -m http.server 8877 --directory dist
```

For embedded audio: `python3 build.py --portable --output out/portable`. For GitHub Pages: `python3 scripts/build_hosted.py`, then `python3 scripts/check_hosted.py`. The Pages workflow builds and deploys on main.

## Authoring and evidence

`course.json` is the complete canonical curriculum; `teaching-pages.json`, `transfer-exercises.json`, `glossary.json`, `course-evidence.json` and `learning-check.json` expose its components for review. `production/af-heart/scenes.json` contains visible transcripts and speech forms with paragraph pauses. `visual-models.json` defines the concept figures. Edit `course.json`, then run `python3 scripts/sync_sources.py`; regenerate any changed recordings before publishing. `scripts/check_content.py` checks alignment and recording-script consistency.

The text and examples were newly authored; the player and café illustration adapt [the social psychology course](https://github.com/snowch/common-ground-social-psychology/tree/5e602bf16bee9f15246aac3afbbeebe377f129df). Sources support the claims but their prose and figures are not reproduced. This is an introductory, AI-assisted course, not an independently reviewed textbook, clinical service or validated personality assessment. Learning effectiveness has not been established in a learner pilot.

Design guidance: [Instructional Design](https://github.com/joelrkohlman/instructional-design/blob/main/SKILL.md) and [Frontend Design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md). Narration: Kokoro v1.0 `af_heart`, speed 1.0, via the separately obtained [record-demo skill](https://github.com/snowch/claude-skills/tree/c9a7c521568632aa216932f4c965df386498602a/plugins/demo-video/skills/record-demo). Automated speech screening is not human listening approval. Fonts and asset notices are included in every edition. See `docs/learning-design.md` and `production/README.md`.

## Validation

Build and curriculum checks use Python’s standard library. Browser checks use Playwright with `/usr/bin/chromium`; expanded accessibility checks use an independently obtained axe-core script (`AXE_SCRIPT`). Set `COURSE_BASE_URL` to the hosted preview or live course. The shared-origin offline check accepts `COURSE_FAMILY_BASE_URL`, `COURSE_COGNITIVE_PATH` and `COURSE_PERSONALITY_PATH` for the two course locations. `COURSE_QA_RESULTS_DIR` can redirect live test artifacts away from the repository.
