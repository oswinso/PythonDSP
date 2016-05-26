from abc import ABC, abstractmethod

class EffectUI(ABC):
	def __init__(self, eventDispatcher):
		self._eventDispatcher = eventDispatcher

	@abstractmethod
	def startGUI(self):
		pass