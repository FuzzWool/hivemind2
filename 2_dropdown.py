from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

##########################################

from code.sfml_plus.ui import ToggleButton

class Dropdown(ToggleButton):
#A dropdown menu which may contain cells.
# LOGIC
	# WIP - Toggle button. Opens and closes.
	# WIP - Remembers the paths/names of selected/hovered cells.
	# WIP - The root parent to Sub_Dropdowns and Cells.

	text = "Dropdown"
	w = 125


##########################################

from code.sfml_plus.ui import Box
from code.sfml_plus.ui import Accept_Button, Cancel_Button
from code.sfml_plus.ui import Horizontal_Slider, Vertical_Slider, SliderBox
# from code.sfml_plus.ui import Slider

Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()
box1.w += 100; box1.h += 100
box1.center = Window.center

box2 = Accept_Button()
box2.x += box1.w - box2.w
box2.y += (box1.h - box2.h) - box2.rise
box1.children.append(box2)

#

dropdown = Dropdown()
dropdown.y += 250
dropdown.x += (box1.w/2) - (dropdown.w/2)
box1.children.append(dropdown)

#

##########################################

while Window.is_open:
	if Window.is_focused:

		if box2.selected\
		or Key.BACKSPACE.pressed():
			box1.close()

		if Key.ENTER.pressed():
			box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display(Mouse)