from app import db
from flask import current_app

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

def get_ordered_event_id():
	return "ordered"

def get_glasses_ready_event_id():
	return "glasses ready"

def get_delivered_event_id():
	return "delivered"
	
def translate_event(id):
	if id == get_ordered_event_id():
		return "besteld"
	elif id == get_glasses_ready_event_id():
		return "glazen klaar"
	elif id == get_delivered_event_id():
		return "afgeleverd"
	return id

def get_event(eventId):
    return Event.query.filter_by(id=eventId).one_or_none()

def get_ordered_event():
	return get_event(get_ordered_event_id())

def get_glasses_ready_event():
	return get_event(get_glasses_ready_event_id())

def get_delivered_event():
	return get_event(get_delivered_event_id())

def get_event_logical_ordering(event):
	if event == get_ordered_event():
		return 0
	elif event == get_glasses_ready_event():
		return 1
	elif event == get_delivered_event():
		return 2
	assert("Extend this list please")

def create_event_if_not_exit(id):
    if get_event(id) is None:
        db.session.add(Event(id=id))

def create_events():
	create_event_if_not_exit(get_ordered_event_id())
	create_event_if_not_exit(get_glasses_ready_event_id())
	create_event_if_not_exit(get_delivered_event_id())
	db.session.commit()