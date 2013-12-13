from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
from code.level_editor.ui import UIBox, Dropdown

#######################################

from code.level_editor.ui import _UI

class TileSelector(_UI):
# WIP - Selects tiles on a Tilesheet.
	# WIP - May store multiple tiles.

	class Cursor:
		pass


#######################################

Window = Window((1200,600), "UI Box (Tile)")

UIBox1 = UIBox()
UIBox1.size = 300,200
UIBox1.center = Window.center
UIBox1.open()

dropdown = Dropdown\
(["a",["A","aa",["C","ca"]],["B","ba",["D","da"]]])
dropdown.center = UIBox1.center
dropdown.y = UIBox1.y2 - dropdown.h
UIBox1.add(dropdown)

Mouse = Mouse(Window)

while Window.is_open:

	if Window.is_focused:
		UIBox1.controls(Key, Mouse, None)

		if Key.ENTER.pressed():
			UIBox1.center = Window.center
			UIBox1.open()
		if Key.BACKSPACE.pressed():
			UIBox1.close()

	Window.clear((255,220,0))
	UIBox1.draw(Window)
	Window.display(Mouse)