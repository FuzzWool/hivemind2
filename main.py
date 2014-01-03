from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

Window = Window((1200, 600), "Hivemind - Demo 2")
Mouse = Mouse(Window)

################################################
from code.game import WorldMap
WorldMap = WorldMap(4,4)

from code.sfml_plus import SmoothCamera
Camera = SmoothCamera(Window)

from code.level_editor import LevelEditor
LevelEditor = LevelEditor(Window)
################################################

while Window.is_open:
	if Window.is_focused:
		LevelEditor.controls(Key, Mouse, Camera)

	Camera.smooth.play()

	Window.clear((255,255,255))
	Window.view = Camera

	LevelEditor.draw_background(Window, Camera)
	WorldMap.draw(Window, Camera)
	LevelEditor.draw_objects(Window, Camera)
	
	Window.display(Mouse)