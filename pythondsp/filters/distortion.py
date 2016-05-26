from effect import Effect
import numpy as np

class Distortion(Effect):
	def __init__(self,dist=0.5):
		Effect.__init__(self,"Distortion Filter")
		self.dist = dist
		self.__class__.__bases__[0].parameters = [dist]

	def applyEffect(self,inputSound):
		k=0
		m = 2*self.dist/(1-self.dist)
		output = (1+m)*inputSound/(1+k*abs(inputSound))
		output = np.array(output,dtype='int16')
		return output