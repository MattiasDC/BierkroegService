from app import db
from flask import current_app

class Product(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Product):
            return self.id == other.id
        return False    

    def __hash__(self):
        return hash(repr(self))

    def can_change_name(self, name):
        products_with_name = Product.query.filter_by(name=name)
        return products_with_name.count() <= 1 and products_with_name.one_or_none() != self

    def delete(self):
        db.session.delete(self)
        
    @classmethod    
    def exist(cls, name):
        return Product.query.filter_by(name=name).one_or_none() is not None

    @classmethod
    def get(cls, id):
        return Product.query.filter_by(id=id).one_or_none()
    
    @classmethod
    def get_all(cls):
        return Product.query.all()
    
    @classmethod
    def create(cls, name):
        product = Product(name=name)
        db.session.add(product)
        return product