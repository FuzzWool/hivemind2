from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
##########################################

from code.sfml_plus import Rectangle

class _UI(Rectangle):
# Communication

	x,y,w,h = 0,0,0,0
	graphics = []

	def controls(self, Key, Mouse, Camera):
		pass

	def draw(self, Window):
		pass


class Box(_UI):
# Graphics
	pass

class Button(_UI):
# State Handling
	pass


##########################################
Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	box1.draw(Window)
	Window.display(Mouse)