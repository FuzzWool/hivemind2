from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

###################################
from code.sfml_plus.ui import Box
from code.sfml_plus.ui import Accept_Button, Cancel_Button
# from code.sfml_plus.ui import Slider

box1 = Box()
box1.w += 100; box1.h += 100
box1.center = Window.center

box2 = Accept_Button()
box2.x += box1.w - box2.w
box2.y += (box1.h - box2.h) - box2.rise
box1.children.append(box2)

box3 = Cancel_Button()
box3.x += box1.w - (box3.w*2)
box3.y += (box1.h - box3.h) - box3.rise
box1.children.append(box3)
###################################

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1
		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	box1.draw(Window)
	Window.display(Mouse)