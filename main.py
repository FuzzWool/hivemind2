from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

Window = Window((1200, 600), "Hivemind - Demo 2")
Mouse = Mouse(Window)

################################################
from code.game import WorldMap
from code.sfml_plus import SmoothCamera
from code.level_editor import LevelEditor

WorldMap = WorldMap(1,1)
WorldMap.tiles[0][0].data = "____"

Camera = SmoothCamera(Window)
LevelEditor = LevelEditor(Window)
################################################

while Window.is_open:
	if Window.is_focused:
		LevelEditor.controls(Key, Mouse, Camera)
		LevelEditor.add_controls(WorldMap)

	Camera.smooth.play()

	Window.clear((255,255,255))
	Window.view = Camera

	LevelEditor.draw_background(Window, Camera)
	WorldMap.draw(Window, Camera)
	LevelEditor.draw_objects(Window, Camera)
	
	Window.display(Mouse)