# Changelog

## 0.1.1

Production bug fix.

- Changed the default Gemini model to `gemini-2.5-flash`.
- Removed newer preview-style model IDs from the default model selector to reduce API-key compatibility failures.
- Added automatic Gemini fallback attempts across Flash models.
- Added clearer API failure messages for invalid keys, unavailable models, network failures, and empty responses.

## 0.1.0

Initial public-ready version.

- Built Streamlit BYOK persona generator.
- Added Google Gemini REST API integration.
- Added beginner-friendly card and menu workflow.
- Added optional "other" fields for menu choices.
- Added expert collaboration text area.
- Added text reference uploads for `txt`, `md`, `csv`, and `json`.
- Added complete prompt preview and prompt download.
- Added persona Markdown download.
- Added next-step action pack in the generation prompt.
- Added Morandi gray and gold visual theme.
- Added gold generate button and API-key notice.
- Added balloons animation after successful generation.
- Added deployment and development documentation.
