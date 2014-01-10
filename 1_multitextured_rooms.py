from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

Window = Window((1200, 600), "Hivemind - Demo 2")
Mouse = Mouse(Window)

################################################
from code.game import WorldMap
from code.sfml_plus import SmoothCamera
from code.level_editor import LevelEditor
from sfml import Texture

WorldMap = WorldMap(10,5)
Camera = SmoothCamera(Window)
LevelEditor = LevelEditor(Window)
################################################

while Window.is_open:
	if Window.is_focused:
		LevelEditor.controls(Key, Mouse, Camera)
		LevelEditor.add_controls(WorldMap)

		if Key.ENTER.pressed():

			#remove test (SUCCESS, completely wiped)
			# for column in WorldMap.rooms[0][0].tiles:
			# 	for tile in column:
			# 		tile.texture = None

			#replace test (SUCCESS, takes on new slot)
			# for column in WorldMap.rooms[0][0].tiles:
			# 	for tile in column:
			# 		tile.texture = "_default/2"

			# #fill test (SUCCESS, error caught)
			# WorldMap.rooms[0][0].tiles[0][0].texture = "_default/1"
			# WorldMap.rooms[0][0].tiles[0][1].texture = "_default/2"
			# WorldMap.rooms[0][0].tiles[0][2].texture = "_default/3"
			# WorldMap.rooms[0][0].tiles[0][3].texture = "_default/4"
			# WorldMap.rooms[0][0].tiles[0][4].texture = "_default/5"

			#replace, replace, replace test (SUCCESS, no problems)
			for column in WorldMap.rooms[0][0].tiles:
				for tile in column:
					tile.texture = "_default/1"
			for column in WorldMap.rooms[0][0].tiles:
				for tile in column:
					tile.texture = "_default/2"
			for column in WorldMap.rooms[0][0].tiles:
				for tile in column:
					tile.texture = "_default/1"



	Camera.smooth.play()

	Window.clear((255,255,255))
	Window.view = Camera

	LevelEditor.draw_background(Window, Camera)
	WorldMap.draw(Window, Camera)
	LevelEditor.draw_objects(Window, Camera)
	
	Window.display(Mouse)