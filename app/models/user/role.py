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

    def translate(self):
        if self.id == Role.get_waiter_id():
            return "opdiener"
        if self.id == Role.get_cash_desk_id():
            return "kassa"
        return self.id

    @classmethod
    def get_admin_id(cls):
        return "admin"
    
    @classmethod
    def get_waiter_id(cls):
        return "waiter"
    
    @classmethod
    def get_cash_desk_id(cls):
        return "cash desk"
    
    @classmethod
    def __create_if_not_exit(cls, id):
        if cls.get(id) is None:
            db.session.add(Role(id=id))
    
    @classmethod
    def create_roles(cls):
        cls.__create_if_not_exit(cls.get_admin_id())
        cls.__create_if_not_exit(cls.get_waiter_id())
        cls.__create_if_not_exit(cls.get_cash_desk_id())
    
    @classmethod
    def get(cls, role_id):
        return Role.query.filter_by(id=role_id).one_or_none()
    
    @classmethod
    def get_admin(cls):
        return cls.get(cls.get_admin_id())
    
    @classmethod
    def get_waiter(cls):
        return cls.get(cls.get_waiter_id())
    
    @classmethod
    def get_cash_desk(cls):
        return cls.get(cls.get_cash_desk_id())
    
    @classmethod
    def get_all(cls):
        return [cls.get_admin(), cls.get_waiter(), cls.get_cash_desk()]