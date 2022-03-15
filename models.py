from sqlalchemy import (Column, Date, Integer, 
                        String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///store_inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Product(Base):
    __tablename__ = "Store Products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column("Name", String)
    product_price = Column("Price", Integer)
    product_quantity = Column("Quantity", Integer)
    product_date = Column("Date Updated", Date)

    
def __repr__(self):
    return  format(f'Product ID: {self.product_id} Name: {self.product_name} Price: {self.product_price} Quantity: {self.product_quantity} Date: {self.product_date}')
    
    
