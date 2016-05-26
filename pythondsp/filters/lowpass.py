from effect import Effect, Parameter
from scipy.signal import butter, lfilter

class LowPass(Effect):

	def __init__(self,cutoff=2000,fs=44100,order=5):
		super(LowPass, self).__init__(self,"Low Pass Filter")
		self.parameters = [Parameter("Cutoff", "Integer 0 -1", cutoff), Parameter("Order", "Integer 0 -1", order)]

	#def createGUI(self):
		#PLACEHOLDER

	def applyEffect(self, inputSound):
		#PLACEHOLDER
		#return inputSound
		cutoff = self.parameters[0].val
		order = self.parameters[1].val

		nyq = self.fs/2
		normalCutoff = cutoff/nyq
		b,a = butter(order,normalCutoff,btype='low',analog=False)
		output = lfilter(b,a,inputSound)
		return output
		

