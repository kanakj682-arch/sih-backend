import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Float, Integer, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class SyncStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class ArtisanProfile(Base):
    __tablename__ = "artisan_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    primary_language: Mapped[str] = mapped_column(String(20), default="hi")
    craft_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    region_state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="artisan")

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    name_hi: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ondc_category_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    artisan_id: Mapped[int] = mapped_column(ForeignKey("artisan_profiles.id"), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)
    
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)
    title_hi: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description_en: Mapped[str] = mapped_column(Text, nullable=False)
    description_hi: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=1)
    
    extracted_features: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    tags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    artisan: Mapped["ArtisanProfile"] = relationship("ArtisanProfile", back_populates="products")
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    sync_logs: Mapped[List["MarketplaceSyncLog"]] = relationship("MarketplaceSyncLog", back_populates="product")

class MarketplaceSyncLog(Base):
    __tablename__ = "marketplace_sync_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    platform_name: Mapped[str] = mapped_column(String(50), nullable=False)
    external_product_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[SyncStatus] = mapped_column(Enum(SyncStatus), default=SyncStatus.PENDING)
    response_payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    synced_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product: Mapped["Product"] = relationship("Product", back_populates="sync_logs")