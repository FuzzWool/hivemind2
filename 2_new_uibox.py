from code.sfml_plus import Window
from code.sfml_plus import Key

Window = Window((1200,600), "Untitled")

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Window.display()