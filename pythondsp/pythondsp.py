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
	chain.setEffect(LowPass(), 0)

	A_freq = 440

	# get timesteps for each sample, T is note duration in seconds
	T = 1
	t = np.linspace(0, T, T * sample_rate, False)

	# generate sine wave notes
	A_note = np.sin(A_freq * t * 2 * np.pi)
	sound = chain.render(A_note)
	#render(sound)
	play(sound)

if __name__ == '__main__':
	main()