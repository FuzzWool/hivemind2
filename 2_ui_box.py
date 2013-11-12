from code.sfml_plus import Window
from code.sfml_plus import key

###################################

from code.sfml_plus import Rectangle
from sfml import RectangleShape
from sfml import Color


class ui_box(Rectangle):
# WIP - Positions UI objects within itself.
	
	def __init__(self):
		self._create_rect()
		self.size = 300,100

	def draw(self, window):
		self._create_rect()
		window.draw(self.rectangle)


	# RECTANGLE

	rectangle = None
	def _create_rect(self): #draw
		rectangle = RectangleShape(self.size)
		rectangle.position = self.position

		rectangle.fill_color = Color(255,150,100)
		rectangle.outline_color = Color.BLACK
		rectangle.outline_thickness = 1
		
		self.rectangle = rectangle



###################################

ui_box = ui_box()
ui_box.position = 100,100


window = Window((1200,600), "UI Box")

while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed(): print 1

	window.clear((255,255,255))
	ui_box.draw(window)
	window.display()