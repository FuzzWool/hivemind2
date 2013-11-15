from code.sfml_plus import Window
from code.sfml_plus import key

############

from sfml import Mouse as _Mouse
from code.sfml_plus import Rectangle

class Mouse(Rectangle):

	def __init__(self, window):
		self.window = window
		self._init_buttons()

	@property
	def x(self):
		return _Mouse.get_position(window.window)[0]
	@property
	def y(self):
		return _Mouse.get_position(window.window)[1]

	#

	# def left_held(self):
	# 	return _Mouse.is_button_pressed(_Mouse.LEFT)

	# def right_held(self):
	# 	return _Mouse.is_button_pressed(_Mouse.RIGHT)

	# def middle_held(self):
	# 	return _Mouse.is_button_pressed(_Mouse.MIDDLE)

	##### BUTTON EVENTS

	def _init_buttons(self): #init
		self.left = left()
		self.right = right()
		self.middle = middle()

	def reset_buttons(self):
		self.left.reset()
		self.right.reset()
		self.middle.reset()

class _Button: #virtual
# . Monitors a 'held' state. Override it.
# * Notes if it has just been pressed or released.
# (Needs to be looped so it refreshes cleanly.)
	
	def held(self): return False

	#

	was_pressed = False
	def pressed(self):
		if self.held() and not self.was_pressed:
			return True
		return False

	def released(self):
		if not self.held() and self.was_pressed:
			return True
		return False

	#

	def reset(self): #Must be called at the end of a loop.
		self.was_pressed = self.held()

class left(_Button):
	def held(self):
		return _Mouse.is_button_pressed(_Mouse.LEFT)

class right(_Button):
	def held(self):
		return _Mouse.is_button_pressed(_Mouse.RIGHT)

class middle(_Button):
	def held(self):
		return _Mouse.is_button_pressed(_Mouse.MIDDLE)



############

window = Window((1200,600), "Untitled")
mouse = Mouse(window)

while window.is_open:
	if window.is_focused:
		if mouse.left.released():
			print mouse.position

	mouse.reset_buttons()

	window.clear((255,220,0))
	window.display()