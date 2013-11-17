from background import Background

class LevelEditor:
# * Contains a background.
# * Handles Camera controls.

	def __init__(self, window):
		self.Background = Background(window)

	def controls(self, key, Camera):
		if key.SPACE.pressed():
			Camera.smooth.room_center =\
			Camera.smooth.room_center

		if key.SPACE.held():
			if key.A.pressed(): Camera.smooth.room_x -= 1
			if key.D.pressed(): Camera.smooth.room_x += 1
			if key.W.pressed(): Camera.smooth.room_y -= 1
			if key.S.pressed(): Camera.smooth.room_y += 1

		else:
			amt = 25
			if key.A.held(): Camera.smooth.x -= amt
			if key.D.held(): Camera.smooth.x += amt
			if key.W.held(): Camera.smooth.y -= amt
			if key.S.held(): Camera.smooth.y += amt

		if key.Q.pressed(): Camera.smooth.zoom /= 2
		if key.E.pressed(): Camera.smooth.zoom *= 2


	def draw(self, window, camera):
		self.Background.draw(window, camera)