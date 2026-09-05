SIH26090: AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans
A production-ready FastAPI backend designed to empower marginalized artisans by providing AI-assisted automatic cataloging in regional languages, CRUD product management, and seamless market linkage integration (ONDC network).

🌟 Key Features
Product Management (CRUD APIs):

Endpoints to create, view, update, and delete artisan products.
Built using SQLAlchemy 2.0 ORM with relational SQLite/PostgreSQL support.
AI Smart Cataloging (POST /api/v1/catalog/auto-generate):

Multimodal endpoint accepting product images and regional speech/text descriptions.
Integrated with Gemini Vision API (with auto-fallback mock data) to automatically extract product features.
Auto-generates bilingual (English + Hindi) SEO titles, descriptions, and category tags.
ONDC Market Linkage Sync (POST /api/v1/marketplaces/sync):

Converts internal database models to standard ONDC (Beckn Protocol) item schemas.
Logs marketplace synchronization attempts with audit status (PENDING, SUCCESS, FAILED).
Automated OpenAPI / Swagger Documentation:

Interactive UI for quick endpoint testing out-of-the-box.
📁 Project Directory Structure
sih-backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # Entry point & FastAPI routes
│   ├── config.py        # Environment settings & Pydantic Config
│   ├── database.py      # SQLAlchemy Engine & Session setup
│   ├── models.py        # Database ORM Models
│   ├── schemas.py       # Pydantic Schemas for data validation
│   ├── ai_service.py    # Gemini Vision AI auto-cataloging service
│   └── ondc_service.py  # ONDC network integration & payload formatting
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation


🚀 Getting Started
1. Prerequisites
Python 3.9 or higher installed.

2. Installation & Virtual Environment
Open your terminal inside the sih-backend directory:

Bash
# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment (Windows)
.\venv\Scripts\activate

# Activate Virtual Environment (Mac/Linux)
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory (already included in repository):

Ini, TOML
PROJECT_NAME="Artisan AI Market Linkage API"
DATABASE_URL="sqlite:///./sih_artisan.db"
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
ONDC_GATEWAY_URL="[https://staging.ondc.org/api/v1](https://staging.ondc.org/api/v1)"
🏃 Running the Application
Start the local FastAPI development server using Uvicorn:

Bash
python -m uvicorn app.main:app --reload --port 8000
Once the server is running, open your browser to access the interactive API documentation:

Interactive Swagger UI Docs: http://127.0.0.1:8000/docs

Alternative ReDoc UI: http://127.0.0.1:8000/redoc

📌 Main API Endpoints Summary
Method	Endpoint	Description
GET	/	Health Check
GET	/api/v1/products/	Get list of artisan products
POST	/api/v1/products/	Create a new artisan product listing
GET	/api/v1/products/{product_id}	Fetch product details by ID
POST	/api/v1/catalog/auto-generate	Upload image + regional audio/text to auto-generate catalog data
POST	/api/v1/marketplaces/sync	Sync an artisan product to ONDC / external marketplaces
🛠 Tech Stack
Framework: FastAPI (Python)

Database ORM: SQLAlchemy 2.0 (SQLite for local testing, PostgreSQL ready)

AI Integration: Google Gemini Generative AI Vision API

Data Validation: Pydantic v2

E-Commerce Standard: ONDC (Beckn Protocol Compatibility)


---
