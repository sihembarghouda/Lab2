# models.py
from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "description": self.description}
