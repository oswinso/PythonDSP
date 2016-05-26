from effectschain import EffectsChain
from filters import *

sample_rate = 44100

def main():
	chain = EffectsChain(1)
	chain.setEffect(delay.Delay(), 0)

	note = [0.5]*100
	sound = chain.render(note)
	#render(sound)
	print(sound)

if __name__ == '__main__':
	main()