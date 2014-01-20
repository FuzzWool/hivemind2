from code.sfml_plus import Window
from code.sfml_plus import Key
################################################

from code.sfml_plus.ui import Box

box1 = Box()
box1.open()

box2 = Box()
box2.follow = False
box2.position = 100,100
box2.follow = False
box1.children.append(box2)

################################################
Window = Window((1200,600), "Untitled")

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed():
			box2.open()

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display()