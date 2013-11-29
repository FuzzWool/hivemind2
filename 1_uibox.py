from code.sfml_plus import Window
from code.sfml_plus import Key

#######################################

class _UIBox:
	pass

class _UIDropdown:
	pass

###############

class UIBox:

	def controls(self):
		pass

	def draw(self):
		pass

	#

	def open(self):
		pass

	def close(self):
		pass

	#####

class UIDropdown:

	def controls(self):
		pass

	def draw(self):
		pass


#######################################


Window = Window((1200,600), "UI Box (Tile)")

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Window.display()