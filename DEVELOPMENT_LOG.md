# Persona Designer Development Log

This document is intended to be used as future AI context. It summarizes what was built, why it was built, the product decisions made, and the current technical state of the project.

## Project Objective

Build a 0-cost Web App named "人物誌設計師 Persona Designer" for marketing users. The app should guide beginners through the required information needed to create useful personas, then generate one or more persona outputs with AI. The app must use a BYOK model: users provide their own Google API Key.

## Source Prompt Reference

The initial product direction came from a local reference file named `Persona Designer.md`. The reference described a professional persona designer prompt in Traditional Chinese. Key requirements from that reference:

- Create detailed, actionable personas.
- Ask for clarification when information is insufficient.
- Cover demographics, goals, motivations, pain points, behaviors, quote, psychographics, values, and actionable insights.
- Avoid stereotypes.
- Use clear, empathetic, practical language.
- Output in a strict Markdown persona format.

The Web App converted this prompt workflow into a guided Streamlit interface.

## Implementation Summary

The app is implemented in `app.py` using Streamlit and direct Gemini REST API calls through `requests`.

Core runtime flow:

1. User enters a Google API Key in the sidebar.
2. User fills guided persona cards.
3. Optional expert notes and uploaded text references are added.
4. App builds a system prompt and user prompt.
5. App calls Gemini `generateContent`.
6. App renders the persona output and provides Markdown download.
7. App triggers Streamlit balloons after successful generation.

The app also supports a manual prompt workflow:

1. User fills the app.
2. App builds the complete prompt.
3. User copies or downloads the prompt.
4. User pastes it into ChatGPT, Gemini, or another LLM.

## Product Decisions

### BYOK

The app follows a Bring Your Own Key model. The Google API Key is entered in a password field and used only in the current Streamlit session. It is not written to disk and is not committed to GitHub.

Reason: keep hosting cost at 0 and avoid managing shared API credentials.

### Beginner-Friendly Input

The original form was too text-heavy. It was redesigned into guided cards:

- 情境卡
- 產品卡
- 受眾卡
- 線索卡
- 痛點卡
- 輸出卡
- 品牌與安全邊界

Each card prioritizes select boxes and multi-select widgets, with short optional text fields for elaboration.

Reason: marketing beginners and AI beginners may not know what to write from scratch. Menus lower the activation energy.

### Expert Collaboration

Added "高手互動區" as an optional free-text area for advanced users.

Purpose: allow experienced marketers to add strategy hypotheses, segmentation logic, research summaries, or special instructions.

### Reference Uploads

Added optional uploads for `txt`, `md`, `csv`, and `json`.

Purpose: improve persona accuracy under a 0-cost development constraint by letting users add real evidence such as interviews, survey summaries, support logs, comments, or sales notes.

Current limit: PDF is not supported yet. A future version can add `pypdf`.

### "Other" Fields

When users select "其他", an optional text field appears.

Reason: keep beginner-friendly menus while preserving flexibility for edge cases.

### Next Step After Persona

The prompt asks the AI to generate a "下一步行動包" after the persona output. This includes concrete next actions and follow-up questions that users can ask an AI LLM.

Reason: users often do not know what to do after receiving personas. The app should anticipate the next workflow.

### Visual Design

The UI evolved through several iterations:

1. Initial neutral marketing UI.
2. More colorful, high-contrast card interface.
3. Final requested theme: Morandi gray background with gold accents.

Current visual decisions:

- Main background: Morandi gray.
- Accent: gold.
- Inputs: dark gray with white text.
- Card top borders: retained as muted multi-color accents.
- Generate button and API key notice: gold.
- Completion delight: Streamlit balloons.

## Current Files

- `app.py`: all Streamlit UI, prompt construction, Gemini API call, file upload handling, and result rendering.
- `requirements.txt`: `streamlit` and `requests`.
- `README.md`: GitHub landing README.
- `DEPLOYMENT.md`: GitHub and Streamlit Community Cloud deployment steps.
- `CHANGELOG.md`: release notes.
- `DEVELOPMENT_LOG.md`: this context file.
- `LICENSE`: MIT license.
- `.gitignore`: excludes virtual environment, cache, secrets, `.env`, and macOS metadata.

## Important Code Concepts

### Prompt Builders

- `build_system_prompt(persona_count)`: builds the role, quality criteria, constraints, and persona Markdown format.
- `build_user_prompt(inputs)`: injects user-selected information, expert notes, uploaded references, generation preferences, and next-step request.
- `build_full_prompt(inputs)`: combines system and user prompt for download/copy workflows.

### Gemini API

- `call_gemini(api_key, model, system_prompt, user_prompt, temperature)`: calls Gemini REST API.
- API URL pattern: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`

### Uploaded References

- `read_uploaded_references(uploaded_files)`: reads text-based uploads.
- Uses UTF-8 decode with `errors="ignore"`.
- Clips total uploaded reference content to around 12,000 characters.

### Optional Other Fields

- `with_other(label, choice, other_value)`: resolves "其他" selections into user-provided values.

## Validation Performed

During development, the following checks were repeatedly run:

```bash
.venv/bin/python -m py_compile app.py
.venv/bin/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py'); at.run(timeout=10); print('errors', len(at.exception)); [print(e.value) for e in at.exception]"
curl -I http://localhost:8501
```

Latest validation status:

- Python compile: passed.
- Streamlit AppTest: `errors 0`.
- Local Streamlit server: returned `HTTP/1.1 200 OK`.

## Current GitHub Publishing State

At the time this log was written:

- The local folder is a Git repository.
- The branch is `main`.
- There is no configured remote.
- GitHub CLI `gh` is not installed in the local environment.
- The available GitHub connector can work with existing installed repositories, but no installed repo matching "Persona Designer" was found.

To publish to GitHub, create a GitHub repository and add it as `origin`, or install/login to GitHub CLI and continue the publish flow.

## Recommended Next Enhancements

1. Add PDF upload support with `pypdf`.
2. Add sample persona project templates for common marketing scenarios.
3. Add an optional "generate interview questions from persona" button.
4. Add an optional "generate content pillars from persona" button.
5. Add browser-level screenshot verification in CI or local Playwright when available.
6. Add model fallback handling when a selected Gemini model is unavailable for a user's API Key.

## Handoff Prompt For Future AI

You are continuing work on a Streamlit project named "Persona Designer" in `/Users/wenanpan/Documents/Persona Designer`. The app is a BYOK Gemini-powered persona generator for marketing beginners and AI beginners. Preserve the current features unless explicitly asked to change them. The current UI theme is Morandi gray with gold accents, dark gray inputs with white text, and muted multi-color card top borders. The app includes beginner cards, expert notes, text uploads, optional "other" fields, complete prompt download, persona Markdown download, next-step action pack, and balloons after successful generation. Validate changes with `py_compile`, Streamlit `AppTest`, and local HTTP check when the server is running.
