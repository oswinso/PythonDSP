from effectschain import EffectsChain
from filters import *

import simpleaudio as sa
import numpy as np
import subprocess as sp

sample_rate = 44100

def play(audio):
	# normalize to 16-bit range if not 16-bit already
	if(audio.dtype != np.int16):
		audio *= 32767 / np.max(np.abs(audio))

		# convert to 16-bit data
		audio = audio.astype(np.int16)

	# start playback
	play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

	# wait for playback to finish before exiting
	#play_obj.wait_done()

def main():
	chain = EffectsChain(10)
	chain.setEffect(highpass.HighPass(1000), 0)

	while True:
		mode = input("Input file? (y/n):")
		sound = 0
		if mode =="y":
			#get the file 
			inFile = input("Enter file name/path: ")
			byteArray = importFile(inFile)
			sound = chain.render(byteArray)

		elif mode == "n":
			freqs = []
			inp = float(input('Enter frequencies: ').strip())
			freqs.append(inp)

			while True:
				try:
					inp = float(input().strip())
					freqs.append(inp)
				except:
					break

			# get timesteps for each sample, T is note duration in seconds
			T = 1
			t = np.linspace(0, T, T * sample_rate, False)

			# generate sine wave notes
			#A_note = np.sin(A_freq * t * 2 * np.pi)
			note = np.sin(freqs[0] * t * 2 * np.pi)
			for i in freqs[1:]:
				note += np.sin(i * t * 2 * np.pi)
			note /= len(freqs)
			sound = chain.render(note)
		else: 
			print("Invalid input!")
		play(sound)

		#commands heres
		while True:
			cmd = input("What would you like to do?") #save file, play, pause (stop?), add filter, remove filter, modify filter, show filters
			if cmd=='s':
				fileName = input("Enter file name:")
				


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

if __name__ == '__main__':
	main()