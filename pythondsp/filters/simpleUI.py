from effect import Parameter

class SimpleUI():

	def __init__(self, parameters, effectDispatcher):
		self._parameters = parameters
		self._state = "param"
		self._paramterIndex = 0
		self._effectDispatcher = effectDispatcher

	def startUI(self):
		while True:
			if self._state == "param":
				parameter = input("Enter Paramter to Edit, or QUIT to exit effec: ").upper()
				if parameter == "QUIT":
					return
				for i in range(0, len(self._parameters)):
					if parameter in self._parameters[i].name.upper():
						self._state = "value"
						self._paramterIndex = i

			if self._state == "value":
				value = input("New value for parameter {}: ".format(parameter))
				if self.isValid(value, self._parameters[i].valOptions):
					self._effectDispatcher.trigger("parameterChanged", self._paramterIndex, float(value))
					self._state = "param"
				else:
					print("Invalid Value")

	def isValid(self, val, valOptions):
		valType, valMin, valMax = valOptions.split(" ")
		valMin = float(valMin)
		valMax = float(valMax)
		try:
			if valType == "Integer":
				val = int(val)
				# Check if valMax is -1, indicating there is no max
				condition = val >= valMin if valMax<valMin else val >= valMin and val <= valMax
				if condition:
					return True
				else:
					print("1")
					return False
			elif valType == "Float":
				val = float(val)
				if val >= valMin and val <= valMax:
					return True
				else:
					print("2")
					return False
		except ValueError:
				print("3")
				return False
		print("4")
		return False