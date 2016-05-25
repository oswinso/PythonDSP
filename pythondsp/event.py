from collections import defaultdict

class Event():
    __events = defaultdict(list)

    @staticmethod
    def on(event, func):
        Event.__events[event].append(func)

    @staticmethod
    def trigger(event, *args, **namedArgs):
        for func in Event.__events[event]:
        	func(*args, **namedArgs)