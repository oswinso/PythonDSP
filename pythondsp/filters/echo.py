from effect import Effect
import queue

class Delay(Effect):

	def __init__(self, decay=0.5, rate=1):
		Effect.__init__(self,"Echo Filter")
		self.decay = decay
		self.rate = rate
		self.__class__.__bases__[0].parameters = [decay,rate]

	#def createGUI(self):
		#PLACEHOLDER

	def applyEffect(self, inputSound):
		ringBuffer = queue.LifoQueue(self.rate * self.fs)
		out[] = []
		for sample in inputSound:
			if not ringBuffer.full():
				output = sample
			else:
				output = (self.decay*ringBuffer.get()+sample)/2
			ringBuffer.put(output)
			out.append(output)
		return output