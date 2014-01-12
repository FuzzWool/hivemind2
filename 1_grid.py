from code.sfml_plus import Window
from code.sfml_plus import Key

from code.sfml_plus import Grid_Room

Window = Window((1200,600), "Untitled")
Grid = Grid_Room()
Grid2 = Grid_Room()
Grid2.room_x = 1

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((0,0,0))
	Window.draw(Grid)
	Window.draw(Grid2)
	Window.display()