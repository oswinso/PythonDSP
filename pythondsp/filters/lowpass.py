from effect import Effect, Parameter
from scipy.signal import butter, lfilter
from filters.simpleUI import SimpleUI

class LowPass(Effect):

	def __init__(self,cutoff=2000,fs=44100,order=5):
		super(LowPass, self).__init__("Low Pass Filter")
		self.parameters = [Parameter("Cutoff", "Integer 0 -1", cutoff), Parameter("Order", "Integer 0 -1", order)]
		self._effectDispatcher.on("parameterChanged", self.onParameterChanged)
		self._UI = SimpleUI(self.parameters, self._effectDispatcher)

	def applyEffect(self, inputSound):
		cutoff = self.parameters[0].val
		order = self.parameters[1].val

		nyq = self.fs/2
		normalCutoff = cutoff/nyq
		b,a = butter(order,normalCutoff,btype='low',analog=False)
		output = lfilter(b,a,inputSound)
		return output
		

