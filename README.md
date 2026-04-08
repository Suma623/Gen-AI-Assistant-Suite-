# GenAI Assistant Suite – Multi-Domain Prompt-Driven AI Platform

## 🌟 Project Overview
GenAI Assistant Suite is a premium, deployable, modular AI Assistant Platform built using Streamlit, Google Gemini 2.5 Flash, and SQLite. This project is meticulously engineered to support specific domains (Education, Healthcare, Finance, Marketing) and provides strict, template-based AI responses to ensure guardrailed accuracy.

It features a fully modernized "SaaS-style" interface, comprehensive browser-cookie session persistence, PDF export functionality, multimodal image input, and integrated Google OAuth login functionality natively hooked to local databases.

## ✨ Features
- **Authentication System**: Dual authentication mechanisms supporting secure `bcrypt` local registrations or Google OAuth 2.0 automatic logins.
- **Persistent Sessions**: State management utilizing native `streamlit-cookies-controller` allowing users to maintain active states seamlessly across standard hard browser refreshes (F5).
- **Advanced Domain Engine**: Restrains AI hallucinations dynamically by prepending strict domain personas and fallback safety guardrails dependent on user selections.
- **Tone & Style Configurations**: Force the output mechanism to return results framed as an "Exam Answer", "Professional", or simple bullet points.
- **Multimodal Upload Array**: Capable of ingesting PDFs (`pypdf`), text streams, or extracting logic from Images hooked securely into Gemini 2.5's vision modalities.
- **Data Persistence**: SQLite-powered backend mapping user history, custom bookmarks, and user qualitative feedback loop tracking.
- **Extract & Download**: Automatically generate downloadable PDF reports of localized AI answers utilizing `FPDF`.
- **Modern Adaptive UX**: Custom-injected CSS providing glassmorphic styling, rounded wrappers, and dynamic auto-syncing between Light and Dark Modes matching system configurations.



## 🛠 Tech Stack
- **Frontend / UX**: Streamlit + Custom injected CSS
- **Backend Core**: Python 3
- **AI Infrastructure**: Google Gemini 2.5 Flash (`google-generativeai`)
- **Database Framework**: SQLite
- **Security & OAuth**: `httpx` (Google Auth Exchange), `bcrypt` (Manual Hashing)
- **Utilities**: `fpdf` (PDFs), `pypdf` (Document parser), `Pillow` (Vision pipeline)

## 📁 Folder Structure
```
GenAI-Assistant-Suite/
├── app.py                   # Central routing & stream interception logic
├── requirements.txt         # Dependency tree
├── .env.example             # Safe variable tracking
├── database/                # SQLite initialization and utility handlers
├── auth/                    # OAuth & manual bcrypt authentication endpoints
├── ui/                      # Dashboard wrappers, aesthetic cards, & theme injections
├── domains/                 # Domain mismatch validation scripts
├── prompts/                 # Core engine assembling context, style, & domain roles
├── ai/                      # Gemini initialization and error-fallback mapping
├── features/                # Integrations (PDF output, image ingestion, suggestions)
├── utils/                   # Shared constant mappings and session cookie re-hydration
└── styles/                  # CSS tokens tracking Dark & Light native implementations
```

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Suma623/Gen-AI-Assistant-Suite-.git
cd Gen-AI-Assistant-Suite-
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Secrets
Duplicate the `.env.example` file and rename it to `.env`. Fill in your specific keys.
```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8501
```

### 5. Initialize the Backend
Run the following script precisely once to generate the `.db` artifact.
```bash
python database/init_db.py
```

### 6. Run the Platform
```bash
streamlit run app.py
```

## 🌍 How to Deploy
This repository is pre-configured to be safely deployed on ephemeral environments natively like **Streamlit Community Cloud** or **Render**. 
Make sure you:
1. Do not push your `.env` or `.db` files!
2. Head into your hosting platform's Dashboard and inject your Environment Secrets into their "Secrets Manager" securely.
3. Hook the `app.py` as your main entry point script!
*(Note: Because standard cloud deployments wipe internal hard-drives on sleep, if you intend to hold permanent active users in deployment, swap out the `sqlite3` driver in `db_utils.py` for a managed backend network connection like Supabase Postgres).*

## 🔮 Future Improvements
- Migration from SQLite to PostgreSQL for multi-region active redundancy.
- Implementing an Admin Dashboard allowing dynamic modification of Prompt Templates globally.
- Integration of Speech-To-Text utilizing Whisper API for accessible prompting logic.

---
*Built organically as a comprehensive demonstration combining rigorous ML Pipeline logic, modular software architecture, and full-stack UX principles.*
