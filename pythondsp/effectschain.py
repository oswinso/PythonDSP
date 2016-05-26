from effect import Effect

class EffectsChain():

	def __init__(self, length=10):
		self.chain = [Effect("") for i in range(length)]

	def setEffect(self, effect, position):
		self.chain[position] = effect

	def rearrange(self, pos1, pos2):
		temp = self.chain[pos1]
		self.chain[pos1] = self.chain[pos2]
		self.chain[pos2] = temp

	def render(self, inputSound):
		output = inputSound
		for effect in self.chain:
			output = effect.getOutput(output)
		return output

	def __str__(self):
		name = "[ "
		for effect in self.chain:
			name += effect.getName()
			name += " "
		name += "]"
		return name

	def __repr__(self):
		name = "[ "
		for effect in self.chain:
			name += effect.getName()
			name += " "
		name += "]"
		return name
