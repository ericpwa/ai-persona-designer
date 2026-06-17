# Persona Designer

「人物誌設計師 Persona Designer」是一個零後端、BYOK 的 Streamlit Web App。它會用卡片、選單與高手自由輸入區，引導使用者整理建立 persona 所需的必要資訊，並透過使用者自備的 Google API Key 呼叫 Gemini API 生成 1 到 5 個可行動的人物誌。

本專案特別為行銷新手與 AI 新手設計：不用一開始就懂 persona、prompt 或市場研究，只要跟著卡片選項填寫，就能得到可用於產品設計、行銷溝通、內容創作、廣告投放與客服訓練的 persona 草稿。

## Demo Flow

1. 在左側輸入自己的 Google API Key。
2. 依序填寫「情境卡、產品卡、受眾卡、線索卡、痛點卡、輸出卡」。
3. 選填「高手互動區」與上傳補充資料。
4. 點擊「生成人物誌」。
5. 取得 persona、下一步行動包，並可下載 Markdown。

## Core Features

- BYOK：使用者自備 Google API Key，Key 只存在本次瀏覽器 session，不寫入檔案。
- 新手友善：用卡片、選單、多選與短文字補充降低填寫門檻。
- 高手互動區：讓有經驗的使用者自由輸入策略假設、研究摘要、受眾切法或判斷。
- 補充資料上傳：0 成本支援 `txt`、`md`、`csv`、`json` 多檔上傳，納入本次 prompt。
- 其他選項補充：使用者選「其他」時會出現選填輸入框。
- 多 persona：一次可生成 1 到 5 個 persona。
- 完整提示詞：可查看、複製、下載完整 prompt，貼到 ChatGPT、Gemini 或其他 LLM。
- 下一步行動包：persona 生成後會提供後續行動與可追問 AI 的問題。
- UI 動效：生成完成後以 Streamlit balloons 提升完成感。
- 0 元發布友善：可部署到 GitHub + Streamlit Community Cloud，不需要資料庫或付費後端。

## Tech Stack

- Python
- Streamlit
- Google Gemini REST API
- requests

## Project Structure

```text
.
├── app.py                # Streamlit Web App
├── requirements.txt      # Python dependencies
├── README.md             # GitHub project README
├── DEPLOYMENT.md         # Deployment guide
├── DEVELOPMENT_LOG.md    # Full development record for future AI context
├── CHANGELOG.md          # Release history
├── LICENSE               # MIT license
└── .gitignore
```

## Quick Start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Google API Key

The app uses the Gemini REST API. Users must provide their own Google API Key in the sidebar.

Do not commit API keys to GitHub. This app does not require `.streamlit/secrets.toml` because it follows a BYOK model.

## Deployment

Recommended free deployment path:

1. Create a GitHub repository.
2. Push this project to GitHub.
3. Open Streamlit Community Cloud.
4. Connect the GitHub repo.
5. Set the main file path to `app.py`.
6. Deploy.

For detailed steps, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Product Notes

The generated persona is a strategy draft, not verified customer research. For better accuracy, upload or paste real evidence such as interviews, survey summaries, customer support logs, social comments, sales notes, or analytics exports.

## License

MIT
