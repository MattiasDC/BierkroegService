from app import db
from flask import current_app

class Role(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.String(128), primary_key=True, nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, User):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(repr(self))

def get_admin_id():
    return "admin"

def create_roles():
    if get_role(get_admin_id()) is None:
        db.session.add(Role(id=get_admin_id()))
    db.session.commit()

def get_role(roleId):
    return Role.query.filter_by(id=roleId).one_or_none()

def get_admin_role():
    return get_role(get_admin_id())