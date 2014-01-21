from sfml import Keyboard
from _button import _Button

class Key:

	pressed = None

	def __init__(self):
		self.create_keys()

	def reset(self): #Window
		for d in self.__dict__:
			if d != "dict_list" and d != "pressed":
				self.__dict__[d].reset()

	#

	def create_keys(self):
		d = self.__dict__
		self.dict_list = []

		#Sort the keys (for Window to ID a key press.)
		import operator
		sorted_Keyboard = \
		sorted(Keyboard.__dict__.iteritems(),\
				key=operator.itemgetter(1))

		#Create my own classes, code by code.
		for i in sorted_Keyboard:
			name, value = i
			if name != "is_key_pressed" \
			and name[:2] != "__":
				if name == "L_CONTROL": name= "L_CTRL"
				if name == "R_CONTROL": name= "R_CTRL"
				if name == "ESCAPE": name= "ESC"
				if name == "RETURN": name= "ENTER"
				if name == "ADD": name= "PLUS"
				if name == "SUBTRACT": name= "MINUS"
				if name == "BACK_SPACE": name="BACKSPACE"
				key = self._key(value, name)
				d[name] = key
				self.dict_list.append(key)


	class _key(_Button):
		def __init__(self, value, name):
			self.value = value
			self.name = name

		def held(self):
			return Keyboard.is_key_pressed(self.value)

Key = Key()