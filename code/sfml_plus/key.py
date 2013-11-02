from sfml import Keyboard

class _key:
# * adds Held and Pressed states.	
# * more readable than sfml defaults

	def __init__(self, value):
		self.value = value
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
	__all__ = set()
	def _track(self): self.__class__.__all__.add(self)
	###


#
for i in Keyboard.__dict__:
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
		vars()[name] = _key(v)

def reset_all():
	for key in _key.__all__:
		key._reset()