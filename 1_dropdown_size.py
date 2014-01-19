from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

################################################

from code.sfml_plus.ui import Box, Dropdown

box1 = Box()
l = [str(i) for i in range(3)]
dropdown1 = Dropdown(l)
dropdown1.w = 50
box1.children.append(dropdown1)
box1.open()
box1.position = 100,100

################################################

Window = Window((1200,600), "Dropdown size adjustments")
Mouse = Mouse(Window)

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1
		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display(Mouse)