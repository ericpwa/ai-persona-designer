import json
from datetime import datetime

import requests
import streamlit as st


APP_TITLE = "Persona Designer"
APP_SUBTITLE = "人物誌設計師"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_MODEL_OPTIONS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-pro",
]
GEMINI_FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]


PERSONA_FORMAT = """
## Persona 名稱: [請為此Persona命名，例如：注重效率的斜槓青年 Alex]

### 👤 人口統計學資訊
* **年齡**: [請填寫具體年齡或範圍]
* **性別**: [請填寫]
* **職業**: [請填寫具體職業或角色]
* **教育程度**: [請填寫]
* **居住地**: [請填寫具體城市或區域]
* **收入範圍**: [請填寫具體範圍或層級]
* **家庭狀況**: [請填寫，例如：單身、已婚有小孩]

### 🎯 目標與動機 (Goals & Motivations)
* **主要目標**: [列出1-3個最核心的目標]
* **次要目標**: [列出其他重要目標]
* **驅動因素**: [解釋是什麼內在或外在因素驅使他們達成這些目標？]

### 😥 痛點與挑戰 (Pain Points & Challenges)
* **主要痛點**: [列出1-3個最主要的困難或問題]
* **次要挑戰**: [列出其他困擾]
* **挫敗來源**: [是什麼讓他們感到沮喪、無助或不滿？]

### 💡 行為模式與偏好 (Behaviors & Preferences)
* **數位行為**: [描述他們常用的社群媒體、網站、App、線上工具等]
* **購物習慣**: [如何研究產品、購買決策流程、偏好線上或實體？]
* **資訊來源**: [他們從哪裡獲取資訊？例如：部落格、KOLs、新聞、專業社群]
* **溝通偏好**: [喜歡哪種溝通方式？例如：Email、即時通訊、電話、面對面]

### 🗣️ 引述 (Quote)
* "[一句代表此Persona核心想法或需求、或常掛在嘴邊的經典語句]"

### 💭 心理特徵與價值觀 (Psychographics & Values)
* **個性特徵**: [列出3-5個形容詞]
* **核心價值觀**: [列出3-5個對他們很重要的價值]
* **對產品/服務/內容情境的態度**: [他們對你正在做的事情有何看法？]

### 🤝 如何滿足此Persona (Actionable Insights)
* **產品/服務設計建議**: [針對此Persona，你的產品或服務應該如何調整或新增功能？]
* **行銷溝通策略**: [針對此Persona，如何選擇管道、訊息、語氣進行行銷？]
* **內容創作方向**: [針對此Persona，應該創作什麼類型、主題的內容？]
* **客戶服務考量**: [在客戶服務上，有哪些需要特別注意的地方？]
"""


def configure_page():
    st.set_page_config(
        page_title=f"{APP_TITLE} | {APP_SUBTITLE}",
        page_icon="👥",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        :root {
            --ink: #252525;
            --muted: #5f625f;
            --line: #3a3a38;
            --paper: #f5f0e7;
            --field: #2f3336;
            --field-line: #b99a57;
            --cyan: #4f9aa0;
            --lime: #8da56b;
            --rose: #b97878;
            --plum: #766b8a;
            --gold: #c7a45c;
        }
        .stApp {
            background:
                linear-gradient(180deg, rgba(203, 202, 194, 0.96) 0%, rgba(176, 177, 171, 0.98) 52%, rgba(143, 145, 141, 1) 100%);
            color: var(--ink);
        }
        .block-container {
            padding-top: 2rem;
            max-width: 1180px;
        }
        [data-testid="stSidebar"] {
            background: #2d3032;
            border-right: 2px solid var(--gold);
        }
        [data-testid="stSidebar"] * {
            color: white;
        }
        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: 0;
        }
        label, .stMarkdown, p, li, span {
            color: var(--ink);
        }
        .hero {
            padding: 2.2rem 2.4rem 1.8rem;
            border: 2px solid var(--line);
            border-radius: 8px;
            background:
                linear-gradient(135deg, rgba(35, 36, 35, 0.94), rgba(93, 91, 86, 0.78), rgba(199, 164, 92, 0.56)),
                url("https://images.unsplash.com/photo-1559136555-9303baea8ebd?auto=format&fit=crop&w=1600&q=80");
            background-size: cover;
            background-position: center;
            min-height: 260px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            box-shadow: 0 24px 0 rgba(51, 50, 47, 0.18);
        }
        .hero h1 {
            color: white;
            font-size: clamp(2.3rem, 4.8vw, 4.8rem);
            line-height: 1;
            margin: 0;
        }
        .hero p {
            max-width: 780px;
            color: rgba(255,255,255,0.96);
            font-size: 1.05rem;
            margin: 1rem 0 0;
        }
        .tiny-label {
            color: #f2d28a;
            text-transform: uppercase;
            font-size: 0.76rem;
            letter-spacing: 0.16em;
            margin-bottom: 0.65rem;
        }
        .section-band {
            padding: 1rem 0 0.35rem;
        }
        .hint {
            color: var(--muted);
            font-size: 0.98rem;
            font-weight: 700;
            line-height: 1.6;
        }
        .guide-card {
            border: 2px solid var(--line);
            border-radius: 8px;
            padding: 1rem 1rem 0.35rem;
            margin: 0.85rem 0 1rem;
            background: rgba(245, 240, 231, 0.97);
            box-shadow: 8px 8px 0 rgba(57, 57, 54, 0.16);
        }
        .guide-card h3 {
            margin: 0 0 0.25rem;
            color: #252525;
            font-size: 1.08rem;
        }
        .guide-card p {
            margin: 0;
            color: #4c4e4b;
            font-weight: 700;
        }
        .card-kicker {
            display: inline-block;
            color: #252525;
            background: var(--gold);
            padding: 0.16rem 0.5rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 800;
            margin-bottom: 0.4rem;
        }
        .card-context { border-top: 8px solid var(--rose); }
        .card-audience { border-top: 8px solid var(--cyan); }
        .card-evidence { border-top: 8px solid var(--lime); }
        .card-output { border-top: 8px solid var(--gold); }
        .metric-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 1rem 0 0.4rem;
        }
        .metric {
            border: 2px solid var(--line);
            border-radius: 8px;
            background: rgba(245, 240, 231, 0.97);
            padding: 0.85rem 1rem;
            box-shadow: 5px 5px 0 rgba(57, 57, 54, 0.14);
        }
        .metric b {
            display: block;
            color: #8c6b2f;
            font-size: 1.2rem;
        }
        .metric span {
            color: #3b3d3b;
            font-size: 0.86rem;
            font-weight: 800;
        }
        .stButton > button, .stDownloadButton > button {
            border-radius: 8px;
            border: 2px solid var(--line);
            background: linear-gradient(135deg, #343638, #8c6b2f);
            color: white;
            font-weight: 800;
            min-height: 3rem;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            border-color: var(--line);
            background: linear-gradient(135deg, #4f5354, #c7a45c);
            color: white;
        }
        .stFormSubmitButton > button {
            border-radius: 8px;
            border: 2px solid var(--line);
            background: linear-gradient(135deg, #c7a45c, #e6c878);
            color: #252525;
            font-weight: 900;
            min-height: 3rem;
        }
        .stFormSubmitButton > button:hover {
            border-color: var(--line);
            background: linear-gradient(135deg, #e6c878, #f2d28a);
            color: #252525;
        }
        .gold-notice {
            border: 2px solid var(--line);
            border-radius: 8px;
            background: linear-gradient(135deg, #c7a45c, #f2d28a);
            color: #252525;
            font-weight: 900;
            padding: 0.85rem 1rem;
            margin: 0.75rem 0;
            box-shadow: 5px 5px 0 rgba(57, 57, 54, 0.14);
        }
        div[data-testid="stTextInput"] input, textarea, div[data-baseweb="select"] {
            border-radius: 8px;
            border-color: var(--field-line);
            color: white;
            background: var(--field);
        }
        div[data-baseweb="select"] * {
            color: white;
        }
        div[data-testid="stTextInput"] input::placeholder, textarea::placeholder {
            color: rgba(255,255,255,0.62);
        }
        [data-testid="stForm"] {
            border: 0;
            background: transparent;
            padding: 0;
        }
        .result-frame {
            border-left: 6px solid var(--gold);
            border-top: 2px solid var(--line);
            border-right: 2px solid var(--line);
            border-bottom: 2px solid var(--line);
            border-radius: 8px;
            background: rgba(245, 240, 231, 0.95);
            padding: 1rem 1rem 1rem 1.1rem;
        }
        @media (max-width: 820px) {
            .hero {
                padding: 1.5rem;
                min-height: 220px;
            }
            .metric-strip {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    defaults = {
        "persona_result": "",
        "last_payload": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def build_gemini_payload(system_prompt, user_prompt, temperature):
    return {
        "systemInstruction": {
            "parts": [{"text": system_prompt}],
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_prompt}],
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "topP": 0.9,
            "maxOutputTokens": 8192,
        },
    }


def parse_gemini_response(response, model):
    if response.status_code != 200:
        try:
            detail = response.json().get("error", {}).get("message", response.text)
        except json.JSONDecodeError:
            detail = response.text
        raise RuntimeError(f"{model}：HTTP {response.status_code} - {detail}")

    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError(f"{model}：Gemini API 沒有回傳候選內容。")

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "\n".join(part.get("text", "") for part in parts).strip()
    if not text:
        finish_reason = candidates[0].get("finishReason", "unknown")
        raise RuntimeError(f"{model}：Gemini API 回傳空白內容，finishReason={finish_reason}。")
    return text


def call_gemini_once(api_key, model, system_prompt, user_prompt, temperature):
    url = GEMINI_API_URL.format(model=model)
    try:
        response = requests.post(
            url,
            params={"key": api_key},
            headers={"Content-Type": "application/json"},
            data=json.dumps(build_gemini_payload(system_prompt, user_prompt, temperature)),
            timeout=90,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"{model}：無法連線到 Gemini API - {exc}") from exc
    return parse_gemini_response(response, model)


def call_gemini(api_key, model, system_prompt, user_prompt, temperature):
    models_to_try = []
    for candidate in [model, *GEMINI_FALLBACK_MODELS]:
        if candidate and candidate not in models_to_try:
            models_to_try.append(candidate)

    errors = []
    for candidate in models_to_try:
        try:
            return call_gemini_once(api_key, candidate, system_prompt, user_prompt, temperature)
        except RuntimeError as exc:
            errors.append(str(exc))

    detail = "\n".join(f"- {error}" for error in errors)
    raise RuntimeError(
        "AI 生成失敗。請先確認 Google API Key 有啟用 Gemini API，且可使用 Gemini Flash 模型。\n\n"
        "本次已自動嘗試多個 Gemini 模型但仍失敗：\n"
        f"{detail}"
    )


def build_system_prompt(persona_count):
    return f"""
你是一位專業的「使用者/客戶 Persona 設計師」，專精於從多元資料中提煉出精準且具洞察力的目標用戶畫像。

請用繁體中文輸出，語氣專業、有同理心、分析性、啟發性，但必須白話、具體、容易理解，特別照顧行銷新手與 AI 新手。

成功標準：
1. 具體且詳細，讓讀者能想像真實個體。
2. 有洞察力，不只列事實，也揭示動機、痛點、未被滿足需求。
3. 有可行動性，行動建議要能直接指導產品、行銷或內容創作。
4. 避免刻板印象，描述要有獨特性與多樣性。
5. 敘述流暢，易讀且有人味。

重要限制：
- 你需要生成 {persona_count} 個 Persona。
- 每個 Persona 都必須完整填寫指定欄位。
- 若資訊不足，請以「待釐清」標示，並用一句話說明為什麼。
- 不要捏造成真實研究結論；若是推論，請自然寫成「可能」、「傾向」、「推測」。
- 每個 Persona 之間需要明顯區隔，不要只是換名字。
- 嚴格使用下列 Markdown 結構，每個 Persona 重複一次：

{PERSONA_FORMAT}
""".strip()


def build_user_prompt(inputs):
    return f"""
請根據以下必要資訊，建立可用於產品設計、行銷溝通、內容創作與客戶服務的人物誌。

【專案情境】
{inputs["project_context"]}

【這次建立 Persona 的目的】
{inputs["persona_goal"]}

【產品/服務/內容描述】
{inputs["offer_description"]}

【目標市場或受眾假設】
{inputs["target_audience"]}

【已知資料或觀察】
{inputs["evidence"]}

【使用者目前遇到的問題或痛點】
{inputs["pain_points"]}

【期待使用者採取的行動】
{inputs["desired_action"]}

【品牌語氣與限制】
{inputs["brand_context"]}

【高手互動區】
{inputs["expert_notes"]}

【上傳補充資料】
{inputs["uploaded_references"]}

【生成偏好】
- Persona 數量：{inputs["persona_count"]}
- 詳細程度：{inputs["depth"]}
- 主要使用場景：{inputs["use_case"]}
- Persona 後的下一步需求：{inputs["next_step"]}
- 請優先避免：{inputs["avoid"]}

請在所有 Persona 後面加上：
1. 「使用提醒」：用 3 個短句提醒行銷新手如何使用這些 Persona。
2. 「下一步行動包」：根據使用者的下一步需求，提供 3 個具體下一步動作，以及 3 個可以繼續問 AI LLM 的追問句。
""".strip()


def completion_score(required_values):
    filled = sum(1 for value in required_values if value and value.strip())
    return filled, len(required_values), int(filled / len(required_values) * 100)


def with_other(label, choice, other_value):
    if choice == "其他" and other_value.strip():
        return f"其他：{other_value.strip()}"
    return choice


def read_uploaded_references(uploaded_files):
    if not uploaded_files:
        return "未上傳補充資料。"

    snippets = []
    remaining_chars = 12000
    for uploaded_file in uploaded_files:
        if remaining_chars <= 0:
            break
        raw = uploaded_file.getvalue()
        text = raw.decode("utf-8", errors="ignore").strip()
        if not text:
            text = "此檔案無法讀取文字內容，請改上傳 txt、md、csv 或 json。"
        clipped = text[: min(len(text), remaining_chars)]
        remaining_chars -= len(clipped)
        snippets.append(
            f"--- 檔名：{uploaded_file.name}；大小：{len(raw)} bytes ---\n{clipped}"
        )

    if remaining_chars <= 0:
        snippets.append("--- 已達本次補充資料讀取上限，後續內容未納入 prompt。---")
    return "\n\n".join(snippets)


def build_full_prompt(inputs):
    return "\n\n".join(
        [
            "【System Prompt】",
            build_system_prompt(inputs["persona_count"]),
            "【User Prompt】",
            build_user_prompt(inputs),
        ]
    )


def render_sidebar():
    with st.sidebar:
        st.markdown("### 啟動設定")
        st.caption("BYOK：你的 Google API Key 只會在本次瀏覽器 session 使用，不會寫入檔案。")
        api_key = st.text_input("Google API Key", type="password", placeholder="AIza...")
        model = st.selectbox(
            "Gemini 模型",
            GEMINI_MODEL_OPTIONS,
            index=GEMINI_MODEL_OPTIONS.index(DEFAULT_GEMINI_MODEL),
            help="建議先用 2.5 Flash。若使用者的 API Key 不支援所選模型，系統會自動嘗試其他 Flash fallback。",
        )
        temperature = st.slider("創意程度", 0.1, 1.0, 0.55, 0.05)
        st.divider()
        st.markdown("### 新手提示")
        st.write("不知道怎麼填時，先用白話寫你已知的事。AI 會把粗略描述整理成可用的人物誌。")
        st.write("資料越具體，Persona 越能拿來做決策；沒有資料也可以標明是假設。")
    return api_key, model, temperature


def render_hero():
    st.markdown(
        f"""
        <div class="hero">
            <div class="tiny-label">BYOK AI WEB APP</div>
            <h1>{APP_TITLE}</h1>
            <p>{APP_SUBTITLE}會引導你把零散的產品想法、客戶觀察與行銷目標整理成可行動的人物誌。適合行銷新手、AI 新手，也適合需要快速產出策略草稿的團隊。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_input_form():
    st.markdown('<div class="section-band">', unsafe_allow_html=True)
    st.subheader("必要資訊")
    st.markdown(
        '<p class="hint">不用一次寫出完整研究報告。先從選單選一個最接近的答案，再用一句話補充你知道的事；AI 會把這些必要資訊整理成人物誌。</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    with st.form("persona_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="guide-card card-context">
                        <span class="card-kicker">STEP 1</span>
                        <h3>情境卡：你正在為什麼做 Persona？</h3>
                        <p>新手先選類型，再補一句話。不要擔心不完整，先讓 AI 知道你的任務輪廓。</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                project_type = st.selectbox(
                    "這次最接近哪一種情境？",
                    ["新產品/新服務上市", "既有產品優化", "行銷策略規劃", "內容創作方向", "廣告投放前分析", "品牌重新定位", "其他"],
                )
                project_type_other = ""
                if project_type == "其他":
                    project_type_other = st.text_input(
                        "其他情境補充（選填）",
                        placeholder="例：投資簡報、會員經營、展店規劃。",
                    )
                persona_goal_choice = st.selectbox(
                    "你希望 Persona 幫你做哪個決策？",
                    ["找出核心客群", "規劃溝通訊息", "設計產品功能", "安排內容主題", "改善轉換流程", "訓練客服/銷售話術", "其他"],
                )
                persona_goal_other = ""
                if persona_goal_choice == "其他":
                    persona_goal_other = st.text_input(
                        "其他決策目的（選填）",
                        placeholder="例：協助業務團隊判斷優先開發名單。",
                    )
                project_context_note = st.text_area(
                    "用一句話補充你的情境",
                    height=90,
                    placeholder="例：我想幫一個新開的線上課程找到第一波最可能購買的人。",
                )

        with col_b:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="guide-card card-output">
                        <span class="card-kicker">STEP 2</span>
                        <h3>產品卡：你要介紹的東西是什麼？</h3>
                        <p>先選成熟度和價格帶，AI 會更容易推測使用者的期待與疑慮。</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                offer_type = st.selectbox(
                    "你的產品/服務/內容屬於哪一類？",
                    ["App / SaaS 工具", "實體商品", "課程 / 顧問 / 教練服務", "內容頻道 / 社群", "活動 / 展覽", "B2B 服務", "其他"],
                )
                offer_type_other = ""
                if offer_type == "其他":
                    offer_type_other = st.text_input(
                        "其他產品/服務類型（選填）",
                        placeholder="例：會員制平台、地方品牌、複合式體驗。",
                    )
                offer_stage = st.selectbox(
                    "目前發展階段",
                    ["只是想法", "MVP / 試營運", "已上市但想成長", "成熟產品想轉型", "尚未確定", "其他"],
                )
                offer_stage_other = ""
                if offer_stage == "其他":
                    offer_stage_other = st.text_input(
                        "其他發展階段（選填）",
                        placeholder="例：募資前、內部測試中、準備改版。",
                    )
                price_level = st.selectbox(
                    "大概價格帶",
                    ["免費 / Freemium", "低單價", "中價位", "高單價 / 高客單", "訂閱制", "尚未定價", "其他"],
                )
                price_level_other = ""
                if price_level == "其他":
                    price_level_other = st.text_input(
                        "其他價格帶（選填）",
                        placeholder="例：依專案報價、抽成制、企業授權。",
                    )
                offer_description_note = st.text_area(
                    "用一句話說明你提供什麼價值",
                    height=90,
                    placeholder="例：幫小品牌把商品賣點快速變成社群貼文和廣告文案。",
                )

        col_c, col_d = st.columns(2)
        with col_c:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="guide-card card-audience">
                        <span class="card-kicker">STEP 3</span>
                        <h3>受眾卡：你猜他們是誰？</h3>
                        <p>還沒有研究資料也沒關係，先把目前假設講清楚，生成結果會標記推論。</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                market_region = st.selectbox(
                    "主要市場",
                    ["台灣", "香港 / 澳門", "華語市場", "日本 / 韓國", "東南亞", "北美", "全球 / 跨區域", "尚未確定", "其他"],
                )
                market_region_other = ""
                if market_region == "其他":
                    market_region_other = st.text_input(
                        "其他主要市場（選填）",
                        placeholder="例：歐洲、澳洲、特定城市或商圈。",
                    )
                audience_role = st.selectbox(
                    "你心中最像的使用者角色",
                    ["一般消費者", "學生 / 新鮮人", "上班族", "自由工作者", "小型企業主", "行銷人員", "專業人士", "家長", "尚未確定", "其他"],
                )
                audience_role_other = ""
                if audience_role == "其他":
                    audience_role_other = st.text_input(
                        "其他使用者角色（選填）",
                        placeholder="例：門市店長、社群小編、非營利組織工作者。",
                    )
                audience_traits = st.multiselect(
                    "他們可能有什麼特徵？",
                    ["時間少", "預算有限", "想學習", "怕踩雷", "重視效率", "重視質感", "需要被教學", "會做很多比較", "願意嘗鮮", "其他"],
                    default=["需要被教學", "會做很多比較"],
                )
                audience_traits_other = ""
                if "其他" in audience_traits:
                    audience_traits_other = st.text_input(
                        "其他受眾特徵（選填）",
                        placeholder="例：需要向主管報告、容易受同儕推薦影響。",
                    )
                target_audience_note = st.text_area(
                    "補充你已知的受眾線索",
                    height=90,
                    placeholder="例：多半是剛開始經營品牌的人，不一定懂行銷術語。",
                )

        with col_d:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="guide-card card-evidence">
                        <span class="card-kicker">STEP 4</span>
                        <h3>線索卡：你目前有什麼根據？</h3>
                        <p>資料可以很粗糙。訪談、留言、客服問題、你的觀察，都能幫 AI 少一點亂猜。</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                evidence_level = st.selectbox(
                    "目前資料成熟度",
                    ["只有初步假設", "有一些社群/客服觀察", "有訪談或問卷", "有銷售/使用數據", "有完整研究資料"],
                )
                evidence_sources = st.multiselect(
                    "你有哪些線索來源？",
                    ["社群留言", "客服訊息", "銷售紀錄", "網站分析", "問卷", "訪談", "競品觀察", "團隊經驗", "暫時沒有", "其他"],
                    default=["團隊經驗"],
                )
                evidence_sources_other = ""
                if "其他" in evidence_sources:
                    evidence_sources_other = st.text_input(
                        "其他線索來源（選填）",
                        placeholder="例：實體活動觀察、通路夥伴回饋。",
                    )
                evidence_note = st.text_area(
                    "補充一個最重要的觀察",
                    height=90,
                    placeholder="例：使用者常問『我不知道第一篇貼文該寫什麼』。",
                )

        col_e, col_f = st.columns(2)
        with col_e:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="guide-card card-context">
                        <span class="card-kicker">STEP 5</span>
                        <h3>痛點卡：他們卡在哪裡？</h3>
                        <p>先勾常見痛點，再補一句你聽過或觀察到的真實說法。</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                pain_categories = st.multiselect(
                    "選出最像的痛點",
                    ["不知道從何開始", "資訊太多難判斷", "時間不夠", "預算不足", "缺乏信任", "操作太複雜", "成效不明顯", "需要主管/夥伴認同", "其他"],
                    default=["不知道從何開始", "資訊太多難判斷"],
                )
                pain_categories_other = ""
                if "其他" in pain_categories:
                    pain_categories_other = st.text_input(
                        "其他痛點（選填）",
                        placeholder="例：組織內部決策慢、資料分散。",
                    )
                frustration_trigger = st.selectbox(
                    "最容易讓他們放棄的是什麼？",
                    ["看不懂專業術語", "不知道下一步", "怕花錢沒效果", "設定流程太麻煩", "找不到適合自己的案例", "需要等待太久", "其他"],
                )
                frustration_trigger_other = ""
                if frustration_trigger == "其他":
                    frustration_trigger_other = st.text_input(
                        "其他放棄原因（選填）",
                        placeholder="例：需要太多跨部門協調。",
                    )
                pain_points_note = st.text_area(
                    "補充一個具體痛點",
                    height=90,
                    placeholder="例：他們常覺得工具很多，但不知道哪個真的適合自己。",
                )

        with col_f:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="guide-card card-output">
                        <span class="card-kicker">STEP 6</span>
                        <h3>輸出卡：你想拿 Persona 做什麼？</h3>
                        <p>這會影響 AI 最後的行動建議，是偏產品、內容、廣告，還是客服。</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                desired_action_choice = st.selectbox(
                    "你希望受眾最後採取什麼行動？",
                    ["註冊試用", "預約諮詢", "購買商品/方案", "訂閱電子報", "加入社群", "下載資料", "觀看內容", "留下名單", "其他"],
                )
                desired_action_other = ""
                if desired_action_choice == "其他":
                    desired_action_other = st.text_input(
                        "其他期待行動（選填）",
                        placeholder="例：參加說明會、分享給主管、完成問卷。",
                    )
                use_case = st.selectbox(
                    "主要使用場景",
                    ["行銷策略", "產品設計", "內容創作", "廣告投放", "客戶服務", "市場研究", "其他"],
                )
                use_case_other = ""
                if use_case == "其他":
                    use_case_other = st.text_input(
                        "其他使用場景（選填）",
                        placeholder="例：業務開發、募資簡報、教育訓練。",
                    )
                next_step = st.selectbox(
                    "拿到 Persona 後，最想接著做什麼？",
                    ["產出行銷訊息", "規劃內容主題", "設計訪談問題", "規劃廣告受眾", "優化產品功能", "設計銷售/客服話術", "其他"],
                )
                next_step_other = ""
                if next_step == "其他":
                    next_step_other = st.text_input(
                        "其他下一步（選填）",
                        placeholder="例：整理成給主管看的策略簡報。",
                    )
                persona_count = st.number_input("Persona 數量", min_value=1, max_value=5, value=1, step=1)
                depth = st.select_slider("詳細程度", options=["快速草稿", "標準", "深入策略版"], value="標準")

        with st.container(border=True):
            st.markdown(
                """
                <div class="guide-card card-audience">
                    <span class="card-kicker">STYLE</span>
                    <h3>品牌與安全邊界</h3>
                    <p>幫 AI 設定語氣和禁區，降低刻板印象與不適合品牌的建議。</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            style_left, style_right = st.columns(2)
            with style_left:
                brand_tone = st.selectbox(
                    "品牌語氣",
                    ["專業但親切", "活潑有趣", "高級精緻", "溫暖陪伴", "直接有力", "理性可信", "其他"],
                )
                brand_tone_other = ""
                if brand_tone == "其他":
                    brand_tone_other = st.text_input(
                        "其他品牌語氣（選填）",
                        placeholder="例：像朋友但不失專業、科技感但不冰冷。",
                    )
                communication_style = st.selectbox(
                    "溝通要多新手友善？",
                    ["像教第一次使用的人", "保留一點專業詞但要解釋", "給有經驗的行銷人看"],
                )
            with style_right:
                avoid_choices = st.multiselect(
                    "請 AI 優先避免",
                    ["性別刻板印象", "年齡刻板印象", "把低預算寫成低價值", "空泛建議", "過度推論", "太學術的語氣"],
                    default=["性別刻板印象", "年齡刻板印象", "空泛建議"],
                )
                brand_note = st.text_input(
                    "其他品牌限制",
                    placeholder="例：避免太強硬的銷售語氣；主要面向台灣市場。",
                )

        with st.container(border=True):
            st.markdown(
                """
                <div class="guide-card card-evidence">
                    <span class="card-kicker">PRO</span>
                    <h3>高手互動區</h3>
                    <p>給已經有想法的使用者自由輸入策略假設、受眾切法、研究摘要或想讓 AI 特別注意的判斷。</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            expert_notes = st.text_area(
                "高手可以直接輸入想法（選填）",
                height=150,
                placeholder="例：我懷疑客群其實分成『自學型創辦人』和『需要顧問陪跑的品牌主』，請生成時特別比較兩者的動機與購買阻力。",
            )
            uploaded_files = st.file_uploader(
                "上傳補充資料（選填，0 成本版支援 txt / md / csv / json）",
                type=["txt", "md", "csv", "json"],
                accept_multiple_files=True,
                help="適合放訪談逐字稿、問卷摘要、客服問題、社群留言、銷售筆記。內容只會送入本次 prompt，不會寫入檔案。",
            )

        project_type_value = with_other("情境類型", project_type, project_type_other)
        persona_goal_value = with_other("決策目的", persona_goal_choice, persona_goal_other)
        offer_type_value = with_other("產品類型", offer_type, offer_type_other)
        offer_stage_value = with_other("發展階段", offer_stage, offer_stage_other)
        price_level_value = with_other("價格帶", price_level, price_level_other)
        market_region_value = with_other("主要市場", market_region, market_region_other)
        audience_role_value = with_other("使用者角色", audience_role, audience_role_other)
        audience_trait_values = [item for item in audience_traits if item != "其他"]
        if audience_traits_other.strip():
            audience_trait_values.append(f"其他：{audience_traits_other.strip()}")
        evidence_source_values = [item for item in evidence_sources if item != "其他"]
        if evidence_sources_other.strip():
            evidence_source_values.append(f"其他：{evidence_sources_other.strip()}")
        pain_category_values = [item for item in pain_categories if item != "其他"]
        if pain_categories_other.strip():
            pain_category_values.append(f"其他：{pain_categories_other.strip()}")
        frustration_trigger_value = with_other("放棄原因", frustration_trigger, frustration_trigger_other)
        desired_action_value = with_other("期待行動", desired_action_choice, desired_action_other)
        use_case_value = with_other("使用場景", use_case, use_case_other)
        next_step_value = with_other("下一步", next_step, next_step_other)
        brand_tone_value = with_other("品牌語氣", brand_tone, brand_tone_other)
        uploaded_references = read_uploaded_references(uploaded_files)

        project_context = "\n".join(
            [
                f"情境類型：{project_type_value}",
                f"補充情境：{project_context_note or '使用者尚未補充，請依情境類型保守推論。'}",
            ]
        )
        persona_goal = f"主要決策目的：{persona_goal_value}"
        offer_description = "\n".join(
            [
                f"產品/服務/內容類型：{offer_type_value}",
                f"發展階段：{offer_stage_value}",
                f"價格帶：{price_level_value}",
                f"價值描述：{offer_description_note or '使用者尚未補充，請標示待釐清並保守推論。'}",
            ]
        )
        target_audience = "\n".join(
            [
                f"主要市場：{market_region_value}",
                f"受眾角色：{audience_role_value}",
                f"可能特徵：{', '.join(audience_trait_values) if audience_trait_values else '尚未選擇'}",
                f"補充線索：{target_audience_note or '使用者尚未補充，請標示待釐清並保守推論。'}",
            ]
        )
        evidence = "\n".join(
            [
                f"資料成熟度：{evidence_level}",
                f"線索來源：{', '.join(evidence_source_values) if evidence_source_values else '尚未選擇'}",
                f"重要觀察：{evidence_note or '使用者尚未補充，請清楚標示推論。'}",
            ]
        )
        pain_points = "\n".join(
            [
                f"痛點類型：{', '.join(pain_category_values) if pain_category_values else '尚未選擇'}",
                f"放棄觸發點：{frustration_trigger_value}",
                f"具體痛點：{pain_points_note or '使用者尚未補充，請標示待釐清並保守推論。'}",
            ]
        )
        desired_action = f"{desired_action_value}；主要使用場景：{use_case_value}"
        brand_context = "\n".join(
            [
                f"品牌語氣：{brand_tone_value}",
                f"新手友善程度：{communication_style}",
                f"其他限制：{brand_note or '未提供。'}",
            ]
        )
        avoid = ", ".join(avoid_choices) if avoid_choices else "避免刻板印象、過度推論與空泛建議。"

        required_values = [
            project_context,
            persona_goal,
            offer_description,
            target_audience,
            evidence,
            pain_points,
            desired_action,
        ]
        filled, total, score = completion_score(required_values)

        st.markdown(
            f"""
            <div class="metric-strip">
                <div class="metric"><b>{score}%</b><span>必要資訊完成度</span></div>
                <div class="metric"><b>{filled}/{total}</b><span>已填必要欄位</span></div>
                <div class="metric"><b>{persona_count}</b><span>預計生成 Persona</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        submitted = st.form_submit_button("生成人物誌", use_container_width=True)

    inputs = {
        "project_context": project_context,
        "persona_goal": persona_goal,
        "offer_description": offer_description,
        "target_audience": target_audience,
        "evidence": evidence,
        "pain_points": pain_points,
        "desired_action": desired_action,
        "brand_context": brand_context or "未提供，請用中性、專業、親切的語氣。",
        "expert_notes": expert_notes or "未提供高手補充想法。",
        "uploaded_references": uploaded_references,
        "avoid": avoid or "避免刻板印象、過度推論與空泛建議。",
        "persona_count": int(persona_count),
        "depth": depth,
        "use_case": use_case_value,
        "next_step": next_step_value,
        "completion": (filled, total, score),
    }
    return submitted, inputs


def render_readiness(inputs, api_key):
    filled, total, score = inputs["completion"]
    missing_labels = []
    required_map = {
        "project_context": "專案情境",
        "persona_goal": "建立目的",
        "offer_description": "產品/服務/內容描述",
        "target_audience": "目標受眾",
        "evidence": "已知資料或觀察",
        "pain_points": "痛點",
        "desired_action": "期待行動",
    }
    for key, label in required_map.items():
        if not inputs[key].strip():
            missing_labels.append(label)

    if not api_key:
        st.markdown(
            '<div class="gold-notice">請先在左側輸入 Google API Key，才能啟動 AI 生成。</div>',
            unsafe_allow_html=True,
        )
    elif score < 100:
        st.info("還差這些必要資訊：" + "、".join(missing_labels))
    else:
        st.success("必要資訊已齊全，可以生成可行動的人物誌。")

    with st.expander("查看或下載完整提示詞", expanded=False):
        full_prompt = build_full_prompt(inputs)
        st.caption("這份提示詞可直接複製到 ChatGPT、Gemini 或其他 LLM；也可以交給本頁 BYOK 模式直接生成。")
        st.code(full_prompt, language="markdown")
        st.download_button(
            "下載完整提示詞",
            data=full_prompt,
            file_name="persona_designer_prompt.md",
            mime="text/markdown",
            use_container_width=True,
        )


def render_results():
    if not st.session_state.persona_result:
        return

    st.divider()
    st.subheader("生成結果")
    st.markdown('<div class="result-frame">', unsafe_allow_html=True)
    st.markdown(st.session_state.persona_result)
    st.markdown("</div>", unsafe_allow_html=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    st.download_button(
        "下載 Markdown",
        data=st.session_state.persona_result,
        file_name=f"persona_designer_{timestamp}.md",
        mime="text/markdown",
        use_container_width=True,
    )


def main():
    configure_page()
    init_state()
    api_key, model, temperature = render_sidebar()
    render_hero()

    submitted, inputs = render_input_form()
    render_readiness(inputs, api_key)

    if submitted:
        filled, total, _ = inputs["completion"]
        if not api_key:
            st.error("尚未輸入 Google API Key。")
        elif filled < total:
            st.error("請先補齊必要資訊，再生成人物誌。")
        else:
            with st.spinner("正在整理洞察、拆分 Persona、生成行動建議..."):
                try:
                    system_prompt = build_system_prompt(inputs["persona_count"])
                    user_prompt = build_user_prompt(inputs)
                    st.session_state.persona_result = call_gemini(
                        api_key=api_key,
                        model=model,
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        temperature=temperature,
                    )
                    st.session_state.last_payload = inputs
                    st.success("人物誌已生成。")
                    st.balloons()
                except Exception as exc:
                    st.error(str(exc))

    render_results()


if __name__ == "__main__":
    main()
