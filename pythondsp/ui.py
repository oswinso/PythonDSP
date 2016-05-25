from effectschain import EffectsChain
from filters import *
import pythondsp as dsp

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
				print("Invalid input")
				self._eventDispatcher.trigger("exit")
			if self._state == "nosound":
				cmd = input("Use an input file? (Y/N):").upper()
				if cmd == 'Y':
					cmd = input("Enter file name:")
					self._eventDispatcher.trigger("importFile", cmd)
					self._state = "main"
				elif cmd == 'N':
					self._eventDispatcher.trigger("synthesizeSound", cmd)
					self._state = "main"
				else:
					self._state = "Invalid"
			if self._state == "main":
				cmd = input("Input a command").upper()
				if cmd == 'P':
					# Dispatch togglePlay event
					self._eventDispatcher.trigger("togglePlay", cmd)
					self._state = "main"
				else:
					self._state = "Invalid command."
					printCommands()

	def printCommands(self):
		print("The available commands are: ......")
