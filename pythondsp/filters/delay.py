from effect import Effect, Parameter
from filters.simpleUI import SimpleUI
import numpy as np

class Delay(Effect):
	def __init__(self, decay=0.5, rate=3):
		super(Delay, self).__init__("Delay")
		self.parameters = [Parameter("Decay", "Float 0 1", decay), Parameter("Rate", "Float 0 -1", rate)]
		self._effectDispatcher.on("parameterChanged", self.onParameterChanged)
		self._UI = SimpleUI(self.parameters, self._effectDispatcher)

	#def createGUI(self):
		#PLACEHOLDER

	def applyEffect(self, inputSound):
		rate = self.parameters[1].val
		decay = self.parameters[0].val

		delayBuffer = inputSound
		maximum = np.amax(inputSound)

		count = 0
		while maximum >= 100: 
			maximum *= decay
			count += 1

		delaySamples = int(self.fs/rate)
		out = [0]*(delaySamples*count + len(inputSound))
		
		for i in range(count + 1):
			delayBufferPos = 0
			for sample in delayBuffer:
				out[i*delaySamples+delayBufferPos] += sample * decay
				delayBufferPos += 1 
			delayBuffer = np.multiply(decay,delayBuffer)

		out = np.asarray(out,dtype=np.int16)
		return out