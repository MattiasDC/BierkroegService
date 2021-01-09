from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

def get_product(id):
    return Product.query.filter_by(id=id).one_or_none()