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
		cmd = ''
		while True:
			if self._state == "invalid":
				print("Invalid input. ")
				self._eventDispatcher.trigger("exit")
			if self._state == "nosound":
				if cmd == '':
					cmd = input("Use an input file? (Y/N): ").upper()
				if cmd == 'Y':
					cmd = input("Enter file name: ")
					try: 
						self._eventDispatcher.trigger("importFile", cmd)
					except: 
						print("File not found.")
						continue
					self._state = "main"
					cmd = ''
				elif cmd == 'N':
					freqstr = input("Enter frequencies, press enter to confirm: ")
					dur = input("Enter the duration in seconds: ")
					freqs = []
					try: 
						freqs = [int(i) for i in freqstr.split(' ')]
						dur = int(dur)
					except: 
						print("Invalid input!")
						continue
					self._eventDispatcher.trigger("synthesizeSound", freqs, dur)
					self._state = "main"
					cmd = ''
				else:
					self._state = "Invalid"
			if self._state == "main":
				if cmd == '':
					cmd = input("Input a command: ").upper()
				if cmd == 'P':
					# Dispatch togglePlay event
					self._eventDispatcher.trigger("togglePlay", "")
					self._state = "main"
					cmd = ''
				elif cmd == "A":
					pos = input("Enter the position of which to add the effect: ")
					name = input("Enter the name of the filter you want to add: ")					
					# Add Effect to EffectsChain
					try: 
						self._eventDispatcher.trigger("addEffect", name, int(pos))
						cmd = ''
					except: 
						print("Effect does not exist!")
				elif cmd == "E":
					pos = input("What is the position of the filter you would like to edit: ")
					try: 
						self._eventDispatcher.trigger("editEffect", int(pos))
						cmd = ''
					except: 
						print("Invalid input!")
					print("")
				elif cmd == "S": 
					filename = input("Enter the file name & format (e.g. example.wav): ")
					try: 
						self._eventDispatcher.trigger("export",filename)
					except: 
						print("Save failed.")
					cmd = ''
				elif cmd == "C": #change file
					print("Changing audio: ")
					self._state = "nosound"
					cmd = ''
				elif cmd == "Q":
					print("Quitting Program.")
					self._eventDispatcher.trigger("exit")
				else:
					print("Invalid command.")
					self.printCommands()
					cmd = ''

	def printCommands(self):
		print("The available commands are: ......")
