from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config import settings
from app.database import Base, engine, get_db
from app.models import Product, MarketplaceSyncLog, SyncStatus
from app.schemas import (
    ProductCreate, ProductResponse, ProductUpdate,
    AICatalogGenerationResponse, MarketplaceSyncRequest, MarketplaceSyncResponse
)
from app.ai_service import AICatalogService
from app.ondc_service import ONDCIntegrationService

# Create Tables in Database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Allow CORS for Frontend/Lovable
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/v1/catalog/auto-generate")
async def generate_catalog():
    return {"status": "success", "message": "Backend connected successfully!"}

@app.get("/")
def root():
    return {"status": "online", "message": "Artisan AI Backend is Running"}

# 1. Product CRUD Routes
@app.post("/api/v1/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/api/v1/products/", response_model=List[ProductResponse])
def list_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

@app.get("/api/v1/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 2. AI Smart Cataloging Endpoint
@app.post("/api/v1/catalog/auto-generate", response_model=AICatalogGenerationResponse)
async def auto_generate_catalog(
    image: UploadFile = File(...),
    audio_transcript_or_text: Optional[str] = Form(None),
    source_language: str = Form("hi")
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    image_bytes = await image.read()
    return await AICatalogService.process_product_catalog(
        image_bytes=image_bytes,
        raw_text_or_transcript=audio_transcript_or_text,
        source_language=source_language
    )

# 3. ONDC Sync Endpoint
@app.post("/api/v1/marketplaces/sync", response_model=MarketplaceSyncResponse)
async def sync_to_marketplaces(payload: MarketplaceSyncRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    sync_result = await ONDCIntegrationService.sync_product_to_ondc(product)
    
    sync_log = MarketplaceSyncLog(
        product_id=product.id,
        platform_name="ONDC",
        external_product_id=sync_result.get("ondc_item_id"),
        status=SyncStatus.SUCCESS,
        response_payload=sync_result
    )
    db.add(sync_log)
    db.commit()

    return MarketplaceSyncResponse(
        product_id=product.id,
        status="SUCCESS",
        sync_details=sync_result
    )