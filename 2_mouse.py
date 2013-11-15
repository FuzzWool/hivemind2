from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)


while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

		if Mouse.left.pressed():
			print Mouse.position

	Window.clear((255,220,0))
	Window.display(Mouse)