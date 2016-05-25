from effect import Effect
import numpy as np

class Delay(Effect):

	def __init__(self, decay=1, rate=1):
		Effect.__init__(self,"Echo Filter")
		self.decay = decay
		self.rate = rate
		self.fs = 44100
		self.__class__.__bases__[0].parameters = [decay,rate]

	#def createGUI(self):
		#PLACEHOLDER

	def applyEffect(self, inputSound):
		'''
		#print("hello")
		delayBuffer = [0] * (int)(self.fs * self.rate)
		delayBufferPos = 0
		out = []
		#print(len(inputSound), len(delayBuffer))
		for sample in inputSound:
			# Delay Algorithm
			output = sample + self.decay * delayBuffer[delayBufferPos]
			out.append(output)

			# Update Delay Buffer
			delayBuffer[delayBufferPos] = sample
			delayBufferPos += 1
			if delayBufferPos == self.fs * self.rate:
				print("hello")
				delayBufferPos = 0
		
				#print("yay")
		#for i in range(0,len(inputSound)):
		#	print("{}, {}".format(inputSound[i],out[i]))
		'''
		delaySamples = int(44100/self.rate)
		out = np.concatenate([inputSound[:],[0]*delaySamples])
		for i in range(len(out)-delaySamples):
			out[i + delaySamples] += float(out[i] * self.decay)
		#for i in range(0,len(inputSound)):
			#print("{}, {}".format(inputSound[i],out[i]))

		out = np.asarray(out,dtype=np.int16)
		return out