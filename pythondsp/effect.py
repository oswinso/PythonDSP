class Effect():

	def __init__(self, name):
		self.name = name
		self.enabled = True
		self.parameters = []

	def getName(self):
		return self.name

	def getOutput(self, inputSound):
		if self.enabled:
			return self.applyEffect(inputSound)
		else:
			return inputSound

	def applyEffect(self, inputSound):
		return inputSound

	def onChangeOption(self, index, val):
		self.parameters[index] = val

	def createGUI(self):
		return