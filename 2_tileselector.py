from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

##########################################

from code.level_editor.ui import TileSelector

##########################################


from code.sfml_plus.ui import Box
from code.sfml_plus.ui import Accept_Button, Cancel_Button

Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()
box1.w += 250; box1.h += 100
box1.center = Window.center

box2 = Accept_Button()
box2.x += box1.w - box2.w
box2.y += (box1.h - box2.h) - box2.rise
box1.children.append(box2)

tileselector = TileSelector()
tileselector.tile_x += 1; tileselector.tile_y += 1
box1.children.append(tileselector)

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