from sfml import Keyboard

class _key:
# * adds Held and Pressed states.	
# * more readable than sfml defaults

	def __init__(self, value, name):
		self.value = value
		self.name = name
		self._track()

	def held(self):
		return Keyboard.is_key_pressed(self.value)

	was_pressed = False
	def pressed(self):
		if not self.was_pressed and self.held():
			return True
		return False

	def _reset(self): #reset_all() (used by window.display)
		self.was_pressed = self.held()


	### INSTANCE TRACKING (reset_all)
	__all__ = []
	def _track(self): self.__class__.__all__.append(self)
	###

#
import operator
sorted_Keyboard = \
sorted(Keyboard.__dict__.iteritems(),\
		key=operator.itemgetter(1))
#
for i in sorted_Keyboard:
	i = i[0]
	if i != "is_key_pressed" \
	and i[:2] != "__":
		v = Keyboard.__dict__[i]
		name = i
		if name == "L_CONTROL": name = "L_CTRL"
		if name == "R_CONTROL": name = "R_CTRL"
		if name == "ESCAPE": name = "ESC"
		if name == "RETURN": name = "ENTER"
		if name == "ADD": name = "PLUS"
		if name == "SUBTRACT": name = "MINUS"
		if name == "BACK_SPACE": name = "BACKSPACE"
		vars()[name] = _key(v, name)


def reset_all():
	for key in _key.__all__:
		key._reset()