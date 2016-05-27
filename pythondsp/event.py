from collections import defaultdict

class Event():
	def __init__(self):
		self._events = defaultdict(list)

	def on(self, event, func):
		self._events[event].append(func)

	def trigger(self, event, *args, **namedArgs):
		for func in self._events[event]:
			func(*args, **namedArgs)