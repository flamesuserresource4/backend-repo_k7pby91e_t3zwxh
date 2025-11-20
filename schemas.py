"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (you can keep or remove as needed):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")


class Software(BaseModel):
    """
    Software catalog schema for the store
    Collection name: "software"
    """
    name: str = Field(..., description="Software name")
    slug: str = Field(..., description="URL-friendly identifier")
    vendor: Optional[str] = Field(None, description="Publisher / Vendor")
    version: Optional[str] = Field(None, description="Version info")
    price: float = Field(..., ge=0, description="Price in USD")
    sale_price: Optional[float] = Field(None, ge=0, description="Optional discounted price in USD")
    license_type: Optional[str] = Field(None, description="e.g., Lifetime, 1-Year, OEM")
    platforms: Optional[List[str]] = Field(default_factory=list, description="Supported platforms")
    thumbnail_url: Optional[str] = Field(None, description="Image URL for product card")
    description: Optional[str] = Field(None, description="Short description of the software")
    featured: bool = Field(False, description="Whether to highlight this product")
