from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200, 600), "Hivemind - Demo 2")

################################################
from code.game import WorldMap
WorldMap = WorldMap(4,4)

from code.sfml_plus import SmoothCamera
Camera = SmoothCamera(window)

from code.level_editor import LevelEditor
LevelEditor = LevelEditor(window)
################################################

while window.is_open:
	if window.is_focused:
		LevelEditor.controls(key, Camera)

	Camera.smooth.play()

	window.clear((255,255,255))
	window.view = Camera

	LevelEditor.draw(window, Camera)
	WorldMap.draw(window, Camera)
	
	window.display()