from code.sfml_plus import Window
from code.sfml_plus import Key

###########################################


###########################################

Window = Window((1200,600), "Untitled")

points = 100,100,300,300
Grid = Grid(points)

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Grid.draw(Window)
	Window.display()