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

def main():
	eventDispatcher = Event()
	eventDispatcher.on("click", test)
	eventDispatcher.trigger("click", "5")

def test(num):
	print("hi, num is {}".format(num))

if __name__ == '__main__':
	main()