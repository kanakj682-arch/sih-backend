from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ProductBase(BaseModel):
    title_en: str
    title_hi: Optional[str] = None
    description_en: str
    description_hi: Optional[str] = None
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0, default=1)
    category_id: Optional[int] = None
    extracted_features: Optional[Dict[str, Any]] = None

class ProductCreate(ProductBase):
    artisan_id: int

class ProductUpdate(BaseModel):
    title_en: Optional[str] = None
    title_hi: Optional[str] = None
    description_en: Optional[str] = None
    description_hi: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    artisan_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AICatalogGenerationResponse(BaseModel):
    title_en: str
    title_hi: str
    description_en: str
    description_hi: str
    suggested_category: str
    detected_craft_type: str
    extracted_features: Dict[str, Any]
    seo_tags: List[str]

class MarketplaceSyncRequest(BaseModel):
    product_id: int
    target_platforms: List[str] = Field(default=["ONDC"])

class MarketplaceSyncResponse(BaseModel):
    product_id: int
    status: str
    sync_details: Dict[str, Any]