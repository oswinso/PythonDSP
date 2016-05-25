from effectschain import EffectsChain
from filters import *
from event import Event
from ui import UI
import sys

import simpleaudio as sa
import numpy as np
import subprocess as sp

class PythonDSP():

	def __init__(self):
		self._UIDispatcher = Event()
		self._sample_rate = 44100

	def initUI(self):
		# Setup UI Dispatcher
		self._UIDispatcher.on("addEffect", "addEffect")
		self._UIDispatcher.on("rearrangeEffect", "rearrangeEffect")
		self._UIDispatcher.on("editEffect", "editEffect")
		self._UIDispatcher.on("togglePlay", "togglePlay")
		self._UIDispatcher.on("export", "export")
		self._UIDispatcher.on("exit", "exit")

		# create UI
		self._UI = UI(self._UIDispatcher)

	def togglePlay(self, audio):
		if(self.isPlaying):
			self.stop()
		else:
			self.play()

	def play(self, audio):
		# normalize to 16-bit range if not 16-bit already
		if(audio.dtype != np.int16):
			audio *= 32767 / np.max(np.abs(audio))

			# convert to 16-bit data
			audio = audio.astype(np.int16)

		# start playback
		this._play_obj = sa.play_buffer(audio, 1, 2, self._sample_rate)

	def addEffect(self, effect, position):
		chain.setEffect(effect, position)

	# rearrange effect in effect chain
	def rearrangeEffect(self, pos1, pos2):
		chain.rearrange(pos1, pos2)

	def editEffect(self):
		pass

	# Blocks until playback done
	def waitTillDone(self):
		play_obj.wait_done()

	# Returns if play_obj is playing
	def isPlaying(self):
		return play_obj.isPlaying()

	# Pause all currently playing things.
	def stop(self):
		play_obj.stop_all()

	def export(self):
		pass

	def exit(self):
		sys.exit()

	'''Imports an audio file with FFMPEG, returns an 
	array of numbers which can be played with simpleaudio'''
	def importFile(fileName):
		FFMPEG_BIN = "ffmpeg"
		FFPROBE_BIN = "ffprobe"

		#use ffmpeg to get file bytes
		openFile = [FFMPEG_BIN,
						'-loglevel','quiet',
						'-i', fileName, 
						'-f', 's16le',
						'-acodec', 'pcm_s16le',
						'-ar', '44100',
						'-ac', '1',
						'-']

		#for determining how many bytes we will need to read
		getLength = [FFPROBE_BIN,
					'-show_entries','format=duration',
					'-loglevel','quiet',
					'-of','default=nokey=1:noprint_wrappers=1',
					fileName]
		filePipe = sp.Popen(openFile, stdout=sp.PIPE,bufsize=10**8)

		raw_audio = filePipe.communicate()[0]

		audio_array = np.fromstring(raw_audio, dtype=np.int16)
		#audio_array = audio_array.reshape((len(audio_array)//2,2))

		return audio_array

def main():
	pythonDSP = PythonDSP()
	pythonDSP.initUI()


if __name__ == '__main__':
	main()