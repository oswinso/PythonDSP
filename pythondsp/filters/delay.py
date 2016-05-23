from effect import Effect
class Delay(Effect):

	def __init__(self, decay=1, rate=1):
		Effect.__init__(self,"Echo Filter")
		self.decay = decay
		self.rate = rate
		self.__class__.__bases__[0].parameters = [decay,rate]

	#def createGUI(self):
		#PLACEHOLDER

	def applyEffect(self, inputSound):
		delayBuffer = [0] * (int)(self.fs * self.rate)
		delayBufferPos = 0
		out = []
		for sample in inputSound:
			# Delay Algorithm
			output = sample + self.decay * delayBuffer[delayBufferPos]
			out.append(output)

			# Update Delay Buffer
			delayBuffer[delayBufferPos] = sample
			delayBufferPos += 1
			if(delayBufferPos == self.fs * self.rate):
				delayBufferPos = 0
				print("yay")
		for i in range(0,len(inputSound)):
			print("{}, {}".format(inputSound[i],out[i]))
		return out