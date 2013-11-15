from sfml import Mouse as _Mouse
from _button import _Button
from code.sfml_plus import Rectangle

class Mouse(Rectangle):

	def __init__(self, window):
		self.window = window
		self._init_buttons()

	#### RECTANGLE

	@property
	def x(self):
		return _Mouse.get_position(self.window.window)[0]
	@property
	def y(self):
		return _Mouse.get_position(self.window.window)[1]

	##### BUTTON EVENTS

	def _init_buttons(self): #init
		self.left = self.left()
		self.right = self.right()
		self.middle = self.middle()

	def reset_buttons(self): #Window
		self.left.reset()
		self.right.reset()
		self.middle.reset()

	class left(_Button):
		def held(self):
			return _Mouse.is_button_pressed(_Mouse.LEFT)

	class right(_Button):
		def held(self):
			return _Mouse.is_button_pressed(_Mouse.RIGHT)

	class middle(_Button):
		def held(self):
			return _Mouse.is_button_pressed(_Mouse.MIDDLE)