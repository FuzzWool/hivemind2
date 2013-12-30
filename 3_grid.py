from code.sfml_plus import Window
from code.sfml_plus import Key

##########################################

from code.sfml_plus import Grid

##########################################

Window = Window((1200,600), "Grid")
Grid = Grid(500,200)

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed():
			Grid.size = 300,300

	Window.clear((255,220,0))
	Window.draw(Grid)
	Window.display()