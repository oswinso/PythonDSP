from effect import Effect, Parameter
from filters.simpleUI import SimpleUI
import numpy as np

class Distortion(Effect):
	def __init__(self,drive=0.5):
		super(Distortion, self).__init__("Distortion")
		self.parameters = [Parameter("Drive", "Float 0 1", drive)]
		self._effectDispatcher.on("parameterChanged", self.onParameterChanged)
		self._UI = SimpleUI(self.parameters, self._effectDispatcher)

	#applies effect to sound
	def applyEffect(self,inputSound):

		drive = self.parameters[0].val
		k=0
		m = 2*drive/(1-drive)
		
		#scale input up
		output = (1+m)*inputSound/(1+k*abs(inputSound))

		#convert output to 16 bit range
		output = np.array(output,dtype='int16')
		return output