from app import db
from flask import current_app

class Product(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Product):
            return self.id == other.id
        return False    

    def __hash__(self):
        return hash(repr(self))