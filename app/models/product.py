from app import db
from flask import current_app

class Product(db.Model):
	__table_args__ = {"schema": current_app.config['DB_SCHEMA']}

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(120), nullable=False)

	def __repr__(self):
		return f'<Product {self.name}>'