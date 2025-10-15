# create_tables.py
from database import engine, Base
from models import Product

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")

if __name__ == "__main__":
    init_db()
