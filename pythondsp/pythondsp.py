from effectschain import EffectsChain
from lowpass import LowPass

import simpleaudio as sa
import numpy as np

sample_rate = 44100

def play(audio):
	# normalize to 16-bit range
	audio *= 32767 / np.max(np.abs(audio))

	# convert to 16-bit data
	audio = audio.astype(np.int16)

	# start playback
	play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

	# wait for playback to finish before exiting
	play_obj.wait_done()

def main():
	chain = EffectsChain(1)
	chain.setEffect(LowPass(500), 0)

	A_freq = 440
	A_h1 = A_freq * 2
	A_h2 = A_freq * 3
	A_h3 = A_freq * 4



	# get timesteps for each sample, T is note duration in seconds
	T = 1
	t = np.linspace(0, T, T * sample_rate, False)

	# generate sine wave notes
	#A_note = np.sin(A_freq * t * 2 * np.pi)
	note = np.sin(A_freq/2 * t * 2 * np.pi) + np.sin(A_h1/2 * t * 2 * np.pi) + np.sin(A_h2/2 * t * 2 * np.pi) + np.sin(A_h3/2 * t * 2 * np.pi) 
	sound = chain.render(note)
	#render(sound)
	play(note)

if __name__ == '__main__':
	main()