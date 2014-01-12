from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

Window = Window((1200, 600), "Hivemind - Demo 2")
Mouse = Mouse(Window)

################################################
from code.game import WorldMap
from code.sfml_plus import SmoothCamera

WorldMap = WorldMap(10,10)
Camera = SmoothCamera(Window)
################################################


while Window.is_open:
	if Window.is_focused:
		pass

	Window.clear((255,255,255))
	Window.view = Camera
	WorldMap.draw(Window, Camera)	
	Window.display(Mouse)