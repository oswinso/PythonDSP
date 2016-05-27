from effectschain import EffectsChain
from filters import *

import simpleaudio as sa
import numpy as np
import subprocess as sp

class UI():
	def __init__(self, eventDispatcher):
		self._eventDispatcher = eventDispatcher
		self._state = "nosound"
		self.start()

	def start(self):
		while True:
			if self._state == "invalid":
				print("Invalid input. ")
				self._eventDispatcher.trigger("exit")
			if self._state == "nosound":
				cmd = input("Use an input file? (Y/N): ").upper()
				if cmd == 'Y':
					cmd = input("Enter file name: ")
					self._eventDispatcher.trigger("importFile", cmd)
					self._state = "main"
				elif cmd == 'N':
					waveform = input("Enter waveform (sine, sawtooth, triangle, square): ").upper()
					freqstr = input("Enter frequencies, press enter to confirm: ")
					dur = input("Enter the duration in seconds: ")
					freqs = []
					try: 
						freqs = [float(i) for i in freqstr.split(' ')]
						print(freqs)
						dur = float(dur)
					except: 
						print("Invalid input!")
						continue
					self._eventDispatcher.trigger("synthesizeSound", waveform, freqs, dur)
					self._state = "main"
				else:
					self._state = "Invalid"
			if self._state == "main":
				cmd = input("Input a command: ").upper()
				if cmd == 'P':
					# Dispatch togglePlay event
					self._eventDispatcher.trigger("togglePlay", "")
					self._state = "main"
				elif cmd == "A":
					name = input("Enter the name of the filter you want to add: ")
					pos = input("Enter the position of which to add the effect: ")
					# Add Effect to EffectsChain
					self._eventDispatcher.trigger("addEffect", name, int(pos))
				elif cmd == "E":
					pos = input("What is the position of the filter you would like to edit: ")
					self._eventDispatcher.trigger("editEffect", int(pos))
					print("")
				elif cmd == "Q":
					print("Quitting Program.")
					self._eventDispatcher.trigger("exit")
				elif cmd == "L":
					self._eventDispatcher.trigger("listFilters")
				else:
					print("Invalid command.")
					self.printCommands()

	def printCommands(self):
		print("The available commands are: ......")
