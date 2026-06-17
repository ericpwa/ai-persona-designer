# Deployment Guide

This project is designed for a 0-cost deployment path using GitHub and Streamlit Community Cloud.

## Local Validation

Run these checks before publishing:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m py_compile app.py
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## GitHub Publishing

If the repository does not exist yet:

1. Create a new GitHub repository named `persona-designer`.
2. Keep it public if you want to use the simplest Streamlit Community Cloud flow.
3. Do not add a README or license in GitHub if you are pushing this local project as the initial commit.

Then run:

```bash
git remote add origin https://github.com/<OWNER>/persona-designer.git
git branch -M main
git push -u origin main
```

## Streamlit Community Cloud

1. Go to Streamlit Community Cloud.
2. Choose "New app".
3. Select the GitHub repository.
4. Branch: `main`.
5. Main file path: `app.py`.
6. Deploy.

No secrets are required for the app itself because it uses BYOK. Each user enters their own Google API Key in the sidebar.

## Post-Deploy Smoke Test

After deployment:

1. Open the deployed app URL.
2. Confirm the sidebar appears.
3. Confirm the Google API Key field is visible.
4. Fill the persona cards with sample data.
5. Generate with a valid Google API Key.
6. Confirm the persona output, Markdown download, full prompt preview, and balloons animation work.

## Known Limits

- Uploaded files are text-only in the first public version: `txt`, `md`, `csv`, `json`.
- PDF upload can be added later with a free dependency such as `pypdf`.
- Generated results should be treated as strategic drafts and validated with real customer evidence.
