from effectschain import EffectsChain
from filters import *

import simpleaudio as sa
import numpy as np
import subprocess as sp

sample_rate = 44100

def play(audio):
	# normalize to 16-bit range
	if(audio.dtype != np.int16):
		audio *= 32767 / np.max(np.abs(audio))

		# convert to 16-bit data
		audio = audio.astype(np.int16)

	# start playback
	play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

	# wait for playback to finish before exiting
	play_obj.wait_done()

def main():
	chain = EffectsChain(10)
	chain.setEffect(highpass.HighPass(1000), 0)

	while True:
		mode = input("Input file? (y/n):")
		if mode =="y":

			inFile = input("Enter file name/path: ")

			byteArray = importFile(inFile)
			outSound = chain.render(byteArray)
			play(outSound)



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
			play(sound)

def importFile(fileName):
	FFMPEG_BIN = "ffmpeg"
	FFPROBE_BIN = "ffprobe"

	openFile = [FFMPEG_BIN,
					'-i', fileName, 
					'-f', 's16le',
					'-acodec', 'pcm_s16le',
					'-ar', '44100',
					'-ac', '2',
					'-']
	getFrames = [FFPROBE_BIN,
				'-v','error',
				'-count_frames',
				'-select_streams', 'a',
				'-show_entries','stream=nb_read_frames',
				'-of','default=nokey=1:noprint_wrappers=1',
				fileName]
	filePipe = sp.Popen(openFile, stdout=sp.PIPE,bufsize=10**8)
	#framePipe = sp.Popen(getFrames, stdout=sp.PIPE)

	#fCount, err = framePipe.communicate()

	raw_audio = filePipe.stdout.read(44100)
	print(raw_audio[-1])
	audio_array = np.fromstring(raw_audio, dtype=np.int16)
	audio_array = audio_array.reshape((len(audio_array)//2,2))

	return audio_array

if __name__ == '__main__':
	main()