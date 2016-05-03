from effect import Effect
#from scipy.signal import butter, lfilter

class LowPass(Effect):

	def __init__(self,cutoff,fs=44100,order=5):
		Effect.__init__(self,"Low Pass Filter")
		self.cutoff = cutoff
		self.fs = fs
		self.order = order
		self.__bases__[0].parameters = [cutoff,fs,order]

	#def createGUI(self):
		#PLACEHOLDER

	def applyEffect(self, inputSound):
		#PLACEHOLDER
		#return inputSound
		nyq = self.fs/2
		normalCutoff = self.cutoff/nyq
		b,a = butter(order,normalCutoff,btype='low',analog=False)
		output = lfilter(b,a,inputSound)
		return output
		
