from event import Event

class Effect(object):

	def __init__(self, name, fs=44100):
		self.name = name
		self.enabled = True
		self.fs = fs
		self.parameters = []
		self._effectDispatcher = Event()

	def getName(self):
		return self.name

	def getOutput(self, inputSound):
		if self.enabled:
			return self.applyEffect(inputSound)
		else:
			return inputSound

	def applyEffect(self, inputSound):
		return inputSound

	def onParameterChanged(self, index, val):
		print("Parameter {} changed to value {}".format(self.parameters[index].name, val))
		self.parameters[index].val = val

	def startUI(self):
		self._UI.startUI()

class Parameter:

	def __init__(self, name, valOptions, val):
		self.name = name
		self.valOptions = valOptions
		self.val = val