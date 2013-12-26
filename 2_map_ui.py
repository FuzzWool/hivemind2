from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

##################################################
from code.sfml_plus import RectangleShape

class Box:
# GRAPHICS
# * Layers - of rectangles. The top and the base.
	
	##############################
	# LOCAL
	children = []

	def __init__(self):
		self.children = []

	def draw(self, Window):
		pass

	##############################
	# CHILDREN
	# WIP - mask/nonmask drawing

	##############################
	# PRIVATE



class ParentBox:
	pass


##################################################

Window = Window((1200,600), "MAP (Mask, Alpha, Position) UI")
Mouse = Mouse(Window)

rect = RectangleShape()
rect.points = 100,100,200,200

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Window.draw(rect)
	Window.display(Mouse)