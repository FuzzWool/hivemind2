from sfml import RenderWindow, VideoMode
from sfml import CloseEvent, FocusEvent
from sfml import Color
from key import reset_all as reset_keys
import key

class Window:
# * Resets the key states every loop.

	def __init__(self, size, name):
		video_mode = VideoMode(*size)
		self.window = RenderWindow(video_mode, name, 4)
		self.window.vertical_synchronization = True


	# Looping
	
	def clear(self, color):
		self._events()
		c = Color(*color)
		self.window.clear(c)

	def display(self):
		reset_keys()
		self.window.display()



	# Simple Forwarding
	
	@property
	def is_open(self): return self.window.is_open
	def close(self): self.window.close()
	def draw(self, *args): self.window.draw(*args)	


	#Event Handling

	is_focused = False

	def _events(self): #clear
		window = self.window

		#use the buttons
		for event in window.events:

			#close the window
			if type(event) is CloseEvent: window.close()
			if key.ESC.pressed(): window.close()

			#toggle focus switch
			if type(event) is FocusEvent:
				self.is_focused = event.gained