from effect import Effect
from scipy.signal import butter, lfilter

class HighPass(Effect):

	def __init__(self,cutoff,fs=44100,order=5):
		Effect.__init__(self,"Low Pass Filter")
		self.cutoff = cutoff
		self.fs = fs
		self.order = order
		self.__class__.__bases__[0].parameters = [cutoff,fs,order]

	#def createGUI(self):
		#PLACEHOLDER

	def applyEffect(self, inputSound):
		#PLACEHOLDER
		#return inputSound
		nyq = self.fs/2
		normalCutoff = self.cutoff/nyq
		b,a = butter(self.order,normalCutoff,btype='high',analog=False)
		output = lfilter(b,a,inputSound)
		return output