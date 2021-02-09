from app import db
from flask import current_app

class Role(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.String(128), primary_key=True, nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Role):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(repr(self))

def get_admin_id():
    return "admin"

def get_waiter_id():
    return "waiter"

def get_cash_desk_id():
    return "cash desk"

def translate_role(id):
    if id == get_waiter_id():
        return "opdiener"
    if id == get_cash_desk_id():
        return "kassa"
    return id

def create_role_if_not_exit(id):
    if get_role(id) is None:
        db.session.add(Role(id=id))
    db.session.commit()

def create_roles():
    create_role_if_not_exit(get_admin_id())
    create_role_if_not_exit(get_waiter_id())
    create_role_if_not_exit(get_cash_desk_id())

def get_role(roleId):
    return Role.query.filter_by(id=roleId).one_or_none()

def get_admin_role():
    return get_role(get_admin_id())

def get_waiter_role():
    return get_role(get_waiter_id())

def get_cash_desk_role():
    return get_role(get_cash_desk_id())

def get_roles():
    return [get_admin_role(), get_waiter_role(), get_cash_desk_role()]