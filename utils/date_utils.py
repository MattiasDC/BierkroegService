from dateutil.parser import parse

def to_date(dateString):
	return parse(dateString).date()

def overlaps(firstStart, firstEnd, secondStart, secondEnd):
	return firstStart < secondEnd and secondStart < firstEnd;