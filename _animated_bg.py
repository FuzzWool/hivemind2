from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200, 600), "Hivemind - Demo 2")

################################################

# class level_editor:
# # WIP - Contains a background.
	
# 	def __init__(self):
# 		pass


################################################

from code.game import WorldMap
WorldMap = WorldMap(4,4)

from code.sfml_plus import SmoothCamera
Camera = SmoothCamera(window)

from code.level_editor import Background
background = Background(window)

while window.is_open:
	if window.is_focused:

		if key.SPACE.pressed():
			Camera.smooth.room_center =\
			Camera.smooth.room_center

		##############
		amt = 25
		if key.A.held(): Camera.smooth.x -= amt
		if key.D.held(): Camera.smooth.x += amt
		if key.W.held(): Camera.smooth.y -= amt
		if key.S.held(): Camera.smooth.y += amt

		if key.Q.pressed(): Camera.smooth.zoom /= 2
		if key.E.pressed(): Camera.smooth.zoom *= 2
		##############

	Camera.smooth.play()

	window.clear((255,255,255))
	window.view = Camera

	background.draw(window, Camera)
	WorldMap.draw(window, Camera)
	
	window.display()