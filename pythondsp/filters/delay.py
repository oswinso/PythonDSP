from effect import Effect, Parameter
from filters.simpleUI import SimpleUI
import numpy as np

class Delay(Effect):
	def __init__(self, decay=0.5, rate=3):
		super(Delay,self).__init__("Delay")
		self.fs = 44100
		self.parameters = [Parameter("Decay", "Float 0 1", decay), Parameter("Rate", "Float 0 -1", rate)]
		self._effectDispatcher.on("parameterChanged", self.onParameterChanged)
		self._UI = SimpleUI(self.parameters, self._effectDispatcher)


	#def createGUI(self):
		#PLACEHOLDER

	def applyEffect(self, inputSound):
		rate = self.parameters[1].val
		decay = self.parameters[0].val

		delayBuffer = [0] * (int)(self.fs * rate)
		delayBufferPos = 0
		out = []
		for sample in inputSound:
			# Delay Algorithm
			output = sample + decay * delayBuffer[delayBufferPos]
			out.append(output)

			# Update Delay Buffer
			delayBuffer[delayBufferPos] = sample
			delayBufferPos += 1
			if delayBufferPos == self.fs * rate:
				delayBufferPos = 0
		#for i in range(0,len(inputSound)):
			#print("{}, {}".format(inputSound[i],out[i]))
		out = np.asarray(out)
		return out