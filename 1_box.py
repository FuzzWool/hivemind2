from code.sfml_plus import Window
from code.sfml_plus import Key

################################################

from code.sfml_plus.ui import Box

Box1 = Box()

################################################

Window = Window((1200,600), "Untitled")

while Window.is_open:
	if Window.is_focused:
		Box1.controls(None,None,None)
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Window.draw(Box1)
	Window.display()