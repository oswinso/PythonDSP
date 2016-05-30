from effectschain import EffectsChain
from filters import *
from effect import Effect
from event import Event
from ui import UI
import scipy
import sys

import importlib

import simpleaudio as sa
import numpy as np
import subprocess as sp

class PythonDSP():

	def __init__(self):
		self._UIDispatcher = Event()
		self._sample_rate = 44100
		self.chain = EffectsChain()
		self._audio = self.getAudioFromFile("default.wav")
		self.play()
		self.stop()
		self.chain = EffectsChain(10)

	def initUI(self):
		# Setup UI Dispatcher
		self._UIDispatcher.on("addEffect", self.addEffect)
		self._UIDispatcher.on("rearrangeEffect", self.rearrangeEffect)
		self._UIDispatcher.on("editEffect", self.editEffect)
		self._UIDispatcher.on("togglePlay", self.togglePlay)
		self._UIDispatcher.on("importFile", self.importFile)
		self._UIDispatcher.on("export", self.export)
		self._UIDispatcher.on("exit", self.exit)
		self._UIDispatcher.on("synthesizeSound", self.synthesizeSound)
		self._UIDispatcher.on("listFilters", self.listFilters)

		# print(globals().keys())

		# create UI
		self._UI = UI(self._UIDispatcher)

	def listFilters(self):
		print(self.chain)

	def togglePlay(self, audio):
		if(self.isPlaying()):
			self.stop()
		else:
			self.play()

	def play(self):
		# normalize to 16-bit range if not 16-bit already
		audio = self.chain.render(self._audio)
		if(audio.dtype != np.int16):
			audio *= 32767 / np.max(np.abs(audio))

			# convert to 16-bit data
			audio = audio.astype(np.int16)

		# start playback
		# self._play_obj = self.getPlayObject(audio)
		self._play_obj = sa.play_buffer(audio, 1, 2, self._sample_rate)

	def synthesizeSound(self, waveform, freqs, duration):
		print(freqs)
		note = self.getWaveform(waveform, freqs[0], duration)
		for i in freqs[1:]:
			note += self.getWaveform(waveform, i, duration)
		self._audio = note

	def getWaveform(self, waveform, freq, duration):
		t = np.linspace(0,duration,duration * self._sample_rate, False)
		if waveform == "SINE":
			note = np.sin(freq * t * 2 * np.pi)
		elif waveform == "SAWTOOTH":
			note = scipy.signal.sawtooth(freq * t * 2 * np.pi)
		elif waveform == "TRIANGLE":
			note = scipy.signal.sawtooth(freq * t * 2 * np.pi, width=0.5)
		elif waveform == "SQUARE":
			note = scipy.signal.square(freq * t * 2 * np.pi)
		return note

	def addEffect(self, effect, position):
		# Convert effect from string to object
		module = globals()[effect.lower()]
		for name in dir(module):
			obj = getattr(module, name)
			try:
				if issubclass(obj, Effect):
					effect = obj()
			except TypeError:
				pass

		# effect = globals()["highpass"].HighPass(cutoff=3000)
		self.chain.setEffect(effect, position)
		self.listFilters()

	# rearrange effect in effect chain
	def rearrangeEffect(self, pos1, pos2):
		self.chain.rearrange(pos1, pos2)

	def editEffect(self, pos):
		self.chain.editEffect(pos)

	# Blocks until playback done
	def waitTillDone(self):
		self._play_obj.wait_done()

	# Returns if play_obj is playing
	def isPlaying(self):
		return self._play_obj.is_playing()

	# Pause all currently playing things.
	def stop(self):
		self._play_obj.stop()

	def export(self,fileName):
		audio = self.chain.render(self._audio)
		saveFile = ["ffmpeg",
						'-f', 's16le',
						'-r','44100',
						'-ac','1',
						'-i','-',
						'-vn',
						fileName]
		#still need to enable directory choices
		pipe = sp.Popen(saveFile,stdin=sp.PIPE,stdout=sp.PIPE, stderr=sp.PIPE)
		pipe.communicate(input=audio.tobytes())

	def exit(self):
		sys.exit()

	'''Imports an audio file with FFMPEG, returns an 
	array of numbers which can be played with simpleaudio'''
	def getAudioFromFile(self, fileName):
		FFMPEG_BIN = "ffmpeg"

		#use ffmpeg to get file bytes
		openFile = [FFMPEG_BIN,
						'-loglevel','quiet',
						'-i', fileName, 
						'-f', 's16le',
						'-acodec', 'pcm_s16le',
						'-ar', '44100',
						'-ac', '1',
						'-']

		filePipe = sp.Popen(openFile, stdout=sp.PIPE,bufsize=10**8)

		raw_audio = filePipe.communicate()[0]

		audio_array = np.fromstring(raw_audio, dtype=np.int16)
		#audio_array = audio_array.reshape((len(audio_array)//2,2))
		if len(audio_array) == 0: 
			raise
		return audio_array

	def importFile(self, fileName):
		self._audio = self.getAudioFromFile(fileName)
		print(fileName)

	def getPlayObject(self, audio):
		return sa.play_buffer(audio, 1, 2, self._sample_rate)

def main():
	pythonDSP = PythonDSP()
	pythonDSP.initUI()

if __name__ == '__main__':
	main()