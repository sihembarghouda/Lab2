# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product as ProductModel
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(title="Product Catalog API", description="A simple API for managing a product catalog")

# Dépendance pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define Pydantic model for Product
class Product(BaseModel):
   id: int
   name: str
   price: float
   description: Optional[str] = None

   class Config:
        orm_mode = True

# GET /products
@app.get("/products", response_model=List[Product])
def list_products(db: Session = Depends(get_db)):
   """Retrieve a list of all products in the catalog."""
   return db.query(ProductModel).all()

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
   """Retrieve a specific product by its ID."""
   product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
   if product is None:
       raise HTTPException(status_code=404, detail="Product not found")
   return product

# POST /products
@app.post("/products", response_model=Product)
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product.id).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product ID already exists")
    new_product = ProductModel(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product