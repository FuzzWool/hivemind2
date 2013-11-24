from sfml import RenderWindow, VideoMode
from sfml import CloseEvent, FocusEvent
from sfml import Color

from code.sfml_plus.graphics import Rectangle

from code.sfml_plus.window import Key
from sfml import KeyEvent


class Window(Rectangle):
# * Resets the key states every loop.

	def __init__(self, size, name):
		video_mode = VideoMode(*size)
		self.window = RenderWindow(video_mode, name, 4)
		self.window.vertical_synchronization = True

		self.position = self.window.position
		self.size = self.window.size


	# Looping
	
	def clear(self, color):
		self._events()
		c = Color(*color)
		self.window.clear(c)

	def display(self, Mouse=None):
		Key.reset()
		if Mouse: Mouse.reset_buttons()
		self.window.display()



	# Simple Forwarding
	@property
	def view(self): return self.window.view
	@view.setter
	def view(self, arg): self.window.view = arg

	@property
	def default_view(self): return self.window.default_view
	@default_view.setter
	def default_view(self, v): self.window.default_view = v

	@property
	def is_open(self): return self.window.is_open
	def close(self): self.window.close()
	def draw(self, *args): self.window.draw(*args)	

	#Event Handling

	is_focused = False
	key_pressed = None


	def _events(self): #clear
		window = self.window

		self.key_pressed = None

		#use the buttons
		for event in window.events:

			# Key currently being typed.
			if type(event) is KeyEvent:
				if event.pressed:
					
					self.key_pressed \
					= Key.dict_list[event.code].name

			#close the window
			if type(event) is CloseEvent: window.close()
			if self.key_pressed == "ESC": window.close()

			#toggle focus switch
			if type(event) is FocusEvent:
				self.is_focused = event.gained