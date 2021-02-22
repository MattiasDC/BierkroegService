from app import db
from flask import current_app
from functools import total_ordering

@total_ordering
class Event(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.String(128), primary_key=True, nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Event):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(repr(self))


    def __lt__(self, other):
        return get_event_logical_ordering(self) < get_event_logical_ordering(other)

    def translate(self):
        if self.id == Event.get_ordered_id():
            return "besteld"
        elif self.id == Event.get_glasses_ready_id():
            return "glazen klaar"
        elif self.id == Event.get_delivered_id():
            return "afgeleverd"
        return self.id

    @classmethod
    def get_ordered_id(cls):
        return "ordered"
    
    @classmethod
    def get_glasses_ready_id(cls):
        return "glasses ready"
    
    @classmethod
    def get_delivered_id(cls):
        return "delivered"
    
    @classmethod
    def get(cls, event_id):
        return Event.query.filter_by(id=event_id).one_or_none()
    
    @classmethod
    def get_ordered(cls):
        return cls.get(cls.get_ordered_id())
    
    @classmethod
    def get_glasses_ready():
        return cls.get(cls.get_glasses_ready_id())
    
    @classmethod
    def get_delivered(cls):
        return cls.get(cls.get_delivered_id())
    
    @classmethod
    def get_event_logical_ordering(cls, event):
        if event == cls.get_ordered():
            return 0
        elif event == cls.get_glasses_ready():
            return 1
        elif event == cls.get_delivered():
            return 2
        assert("Extend this list please")
    
    @classmethod
    def __create_if_not_exit(cls, id):
        if cls.get(id) is None:
            db.session.add(Event(id=id))
    
    @classmethod
    def create_events(cls):
        cls.__create_if_not_exit(cls.get_ordered_id())
        cls.__create_if_not_exit(cls.get_glasses_ready_id())
        cls.__create_if_not_exit(cls.get_delivered_id())
        db.session.commit()