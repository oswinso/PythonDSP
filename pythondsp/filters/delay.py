from effect import Effect
import numpy as np

class Delay(Effect):
	def __init__(self, decay=0.5, rate=3):
		Effect.__init__(self,"Echo Filter")
		self.decay = decay
		self.rate = rate
		self.fs = 44100
		self.__class__.__bases__[0].parameters = [decay,rate]

	#def createGUI(self):
		#PLACEHOLDER

	def applyEffect(self, inputSound):
		
		#print("hello")
		delayBuffer = inputSound

		maximum = np.amax(inputSound)

		count = 0
		while maximum >= 100: 
			maximum *= self.decay
			count += 1

		delaySamples = int(self.fs/self.rate)
		out = [0]*(delaySamples*count + len(inputSound))
		
		for i in range(count + 1):
			delayBufferPos = 0
			for sample in delayBuffer:
				out[i*delaySamples+delayBufferPos] = sample * self.decay
				delayBufferPos += 1 
			delayBuffer = np.multiply(self.decay,delayBuffer)

		out = np.asarray(out,dtype=np.int16)
		return out