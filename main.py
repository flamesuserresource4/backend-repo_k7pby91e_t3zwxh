import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId

from database import create_document, get_documents, db
from schemas import Software as SoftwareSchema

app = FastAPI(title="Software Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SoftwareCreate(BaseModel):
    name: str
    slug: str
    vendor: Optional[str] = None
    version: Optional[str] = None
    price: float
    sale_price: Optional[float] = None
    license_type: Optional[str] = None
    platforms: Optional[List[str]] = []
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None
    featured: bool = False


def serialize_doc(doc: dict) -> dict:
    if not doc:
        return doc
    d = {**doc}
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    # convert any nested ObjectIds just in case
    for k, v in list(d.items()):
        if isinstance(v, ObjectId):
            d[k] = str(v)
    return d


@app.get("/")
def read_root():
    return {"message": "Software Store Backend Running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response


DEFAULT_SOFTWARE = [
    {
        "name": "Microsoft Office",
        "slug": "ms-office",
        "vendor": "Microsoft",
        "version": "2021",
        "price": 149.0,
        "license_type": "Lifetime",
        "platforms": ["Windows", "macOS"],
        "thumbnail_url": "https://images.unsplash.com/photo-1548611716-69b2d3cb83de?w=600&q=80&auto=format&fit=crop",
        "description": "Word, Excel, PowerPoint, and more.",
        "featured": True,
    },
    {
        "name": "Autodesk AutoCAD",
        "slug": "autodesk-autocad",
        "vendor": "Autodesk",
        "version": "2024",
        "price": 299.0,
        "license_type": "1-Year",
        "platforms": ["Windows"],
        "thumbnail_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600&q=80&auto=format&fit=crop",
        "description": "Design and drafting software.",
        "featured": False,
    },
    {
        "name": "Adobe Photoshop",
        "slug": "adobe-photoshop",
        "vendor": "Adobe",
        "version": "2024",
        "price": 199.0,
        "license_type": "Lifetime",
        "platforms": ["Windows", "macOS"],
        "thumbnail_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&q=80&auto=format&fit=crop",
        "description": "Image editing and compositing.",
        "featured": True,
    },
    {
        "name": "Adobe After Effects",
        "slug": "adobe-after-effects",
        "vendor": "Adobe",
        "version": "2024",
        "price": 179.0,
        "license_type": "Lifetime",
        "platforms": ["Windows", "macOS"],
        "thumbnail_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=80&auto=format&fit=crop",
        "description": "Motion graphics and VFX.",
        "featured": False,
    },
    {
        "name": "Adobe Premiere Pro",
        "slug": "adobe-premiere-pro",
        "vendor": "Adobe",
        "version": "2024",
        "price": 189.0,
        "license_type": "Lifetime",
        "platforms": ["Windows", "macOS"],
        "thumbnail_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=600&q=80&auto=format&fit=crop",
        "description": "Video editing for creators.",
        "featured": True,
    },
    {
        "name": "Adobe Illustrator",
        "slug": "adobe-illustrator",
        "vendor": "Adobe",
        "version": "2024",
        "price": 169.0,
        "license_type": "Lifetime",
        "platforms": ["Windows", "macOS"],
        "thumbnail_url": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?w=600&q=80&auto=format&fit=crop",
        "description": "Vector graphics and illustration.",
        "featured": False,
    },
    {
        "name": "CorelDRAW Graphics Suite",
        "slug": "coreldraw",
        "vendor": "Corel",
        "version": "2023",
        "price": 159.0,
        "license_type": "Lifetime",
        "platforms": ["Windows"],
        "thumbnail_url": "https://images.unsplash.com/photo-1523475496153-3d6cc0d0f389?w=600&q=80&auto=format&fit=crop",
        "description": "Professional graphic design software.",
        "featured": False,
    },
    {
        "name": "Windows 11 Pro",
        "slug": "windows-11-pro",
        "vendor": "Microsoft",
        "version": "11",
        "price": 99.0,
        "license_type": "OEM",
        "platforms": ["Windows"],
        "thumbnail_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&q=80&auto=format&fit=crop",
        "description": "Latest Windows operating system.",
        "featured": True,
    },
    {
        "name": "Windows 10 Pro",
        "slug": "windows-10-pro",
        "vendor": "Microsoft",
        "version": "10",
        "price": 79.0,
        "license_type": "OEM",
        "platforms": ["Windows"],
        "thumbnail_url": "https://images.unsplash.com/photo-1517433456452-f9633a875f6f?w=600&q=80&auto=format&fit=crop",
        "description": "Trusted Windows OS.",
        "featured": False,
    },
    {
        "name": "Windows 7 Pro",
        "slug": "windows-7-pro",
        "vendor": "Microsoft",
        "version": "7",
        "price": 49.0,
        "license_type": "OEM",
        "platforms": ["Windows"],
        "thumbnail_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&q=80&auto=format&fit=crop",
        "description": "Legacy Windows OS for older PCs.",
        "featured": False,
    },
]


@app.get("/api/software")
def list_software():
    # seed if empty
    count = db["software"].count_documents({}) if db is not None else 0
    if count == 0:
        for item in DEFAULT_SOFTWARE:
            model = SoftwareSchema(**item)
            create_document("software", model)
    docs = get_documents("software")
    return [serialize_doc(d) for d in docs]


@app.post("/api/software", status_code=201)
def add_software(payload: SoftwareCreate):
    model = SoftwareSchema(**payload.model_dump())
    inserted_id = create_document("software", model)
    return {"id": inserted_id}


@app.get("/api/software/{slug}")
def get_software_by_slug(slug: str):
    doc = db["software"].find_one({"slug": slug}) if db is not None else None
    if not doc:
        raise HTTPException(status_code=404, detail="Software not found")
    return serialize_doc(doc)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
