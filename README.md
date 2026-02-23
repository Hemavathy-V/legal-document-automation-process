# Legal Document Automation Process

A full-stack Legal Contract Management System that enables lawyers, admins, and clients to manage, review, and generate legal contracts with AI-assisted template processing.

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | React 18 + Vite                     |
| Backend  | FastAPI (Python)                    |
| Database | MySQL                               |
| Auth     | JWT (python-jose + passlib/bcrypt)  |

---

## Project Structure

```
legal-document-automation-process/
├── .env                         # Local secrets (git-ignored)
├── .env.example                 # Template — copy to .env and fill in values
├── .gitignore
├── README.md
│
├── backend/
│   ├── __init__.py
│   ├── requirements.txt         # Python dependencies
│   ├── logger.py                # Centralised logging configuration
│   ├── database/                # Python database layer
│   │   ├── __init__.py
│   │   └── db_connection.py     # MySQL connection factory
│   ├── scripts/                 # Standalone data-pipeline utilities
│   │   ├── fetch_templates.py   # Copy template files from DB records → output/
│   │   └── ingest_templates.py  # Parse DOCX files and load into MySQL
│   └── app/                     # FastAPI application
│       ├── main.py              # App factory, CORS, router registration
│       ├── auth.py              # JWT creation / verification
│       ├── deps.py              # Shared FastAPI dependencies (current user)
│       ├── schemas.py           # Pydantic request / response models
│       ├── routers/
│       │   ├── login_router.py      # POST /api/login, POST /api/register
│       │   ├── contracts_router.py  # GET /api/contracts
│       │   └── templates_router.py  # GET /api/templates
│       └── prompts/
│           └── legal_contract_prompt.py  # AI prompt template (future use)
│
├── database/
│   └── init/                    # Ordered DDL + seed scripts (SQL only)
│       ├── 0-init.sql           # Schema: look_up, users, contracts
│       ├── 1-init.sql           # Seed data: lookup values, users, contracts
│       └── 2-init.sql           # Schema + seed: contract_templates
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.mts          # Vite dev server + /api proxy to :8000
    └── src/
        ├── App.jsx              # Root component (login gate + pages)
        ├── main.jsx
        ├── styles.css
        ├── api/                 # Fetch wrappers per feature
        │   ├── common.js
        │   ├── login.js
        │   ├── contracts.js
        │   └── templates.js
        └── pages/
            ├── login/
            │   └── LoginPage.jsx
            ├── contracts/
            │   ├── ContractsPage.jsx
            │   └── ContractsTable.jsx
            └── templates/
                ├── TemplatesPage.jsx
                └── TemplatesTable.jsx
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8+

### 1. Clone & configure environment

```bash
cp .env.example .env
# Edit .env with your database credentials and a strong SECRET_KEY
```

### 2. Database setup

Run the init scripts in order against your MySQL instance:

```bash
mysql -u root -p < database/init/0-init.sql
mysql -u root -p < database/init/1-init.sql
mysql -u root -p < database/init/2-init.sql
```

### 3. Backend

```bash
cd backend
pip install -r requirements.txt

# Run from the project root so package imports resolve correctly
cd ..
uvicorn backend.app.main:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at: `http://localhost:5173`

---

## Utility Scripts

Run from the **project root** so `backend.*` imports resolve:

```bash
# Copy template files from DB records into output/
python -m backend.scripts.fetch_templates

# Ingest DOCX files from sample_templates/ into the database
python -m backend.scripts.ingest_templates --templates-dir sample_templates --version v1.0
```

---

## API Endpoints

| Method | Path              | Auth     | Description                    |
|--------|-------------------|----------|--------------------------------|
| POST   | /api/login        | Public   | Login — returns JWT + user     |
| POST   | /api/register     | Public   | Register a new user            |
| GET    | /api/contracts    | JWT      | List all contracts             |
| GET    | /api/templates    | JWT      | List all contract templates    |
| GET    | /health           | Public   | Health check                   |

---

## Default Seed Users

All seed users have the password `Password1`.

| Name          | Email                         | Role             |
|---------------|-------------------------------|------------------|
| Arun Kumar    | arun.kumar@company.com        | Lawyer           |
| Meena Sharma  | meena.sharma@company.com      | Admin            |
| Ravi Patel    | ravi.patel@client.com         | Client           |
| Sanjay Rao    | sanjay.rao@company.com        | Assistant Lawyer |
| Anita Verma   | anita.verma@company.com       | Admin            |
