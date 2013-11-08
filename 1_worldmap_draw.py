from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200, 600), "Hivemind - Demo 2")

################################################

from code.game import WorldMap
WorldMap = WorldMap(4,4)

from code.sfml_plus import SmoothCamera
Camera = SmoothCamera(window)

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

	window.clear((255,220,0))
	window.view = Camera
	WorldMap.draw(window, Camera)
	window.display()