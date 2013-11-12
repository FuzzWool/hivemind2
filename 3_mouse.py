from code.sfml_plus import Window
from code.sfml_plus import key

############

from sfml import Mouse as _Mouse
from code.sfml_plus import Rectangle
class Mouse(Rectangle):

	def __init__(self, window):
		self.window = window

	@property
	def x(self):
		return _Mouse.get_position(window.window)[0]
	@property
	def y(self):
		return _Mouse.get_position(window.window)[1]

	#

	def left_held(self):
		return _Mouse.is_button_pressed(_Mouse.LEFT)

	def right_held(self):
		return _Mouse.is_button_pressed(_Mouse.RIGHT)

	def middle_held(self):
		return _Mouse.is_button_pressed(_Mouse.MIDDLE)

############

window = Window((1200,600), "Untitled")
mouse = Mouse(window)

while window.is_open:
	if window.is_focused:
		if mouse.left_held():
			print mouse.position

	window.clear((255,220,0))
	window.display()