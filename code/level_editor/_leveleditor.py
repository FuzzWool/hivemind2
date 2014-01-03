from background import Background
from toolbox import ToolBox

class LevelEditor:
# * Contains a background.
# * Handles Camera controls.

	def __init__(self, window):
		self.Background = Background(window)
		self.ToolBox = ToolBox(*window.size)

	def controls(self, Key, Mouse, Camera):
		#toolbox
		self.ToolBox.controls(Key, Mouse, Camera)
		if Key.TAB.pressed(): self.ToolBox.toggle()

		#general
		if Key.SPACE.pressed():
			Camera.smooth.room_center =\
			Camera.smooth.room_center

		if Key.SPACE.held():
			if Key.A.pressed(): Camera.smooth.room_x -= 1
			if Key.D.pressed(): Camera.smooth.room_x += 1
			if Key.W.pressed(): Camera.smooth.room_y -= 1
			if Key.S.pressed(): Camera.smooth.room_y += 1

		else:
			amt = 25
			if Key.A.held(): Camera.smooth.x -= amt
			if Key.D.held(): Camera.smooth.x += amt
			if Key.W.held(): Camera.smooth.y -= amt
			if Key.S.held(): Camera.smooth.y += amt

		if Key.Q.pressed(): Camera.smooth.zoom /= 2
		if Key.E.pressed(): Camera.smooth.zoom *= 2


	def add_controls(self, WorldMap):
		self.ToolBox.add_controls(WorldMap)

	def draw_background(self, Window, Camera):
		self.Background.draw(Window, Camera)

	def draw_objects(self, Window, Camera):
		Window.view = Window.default_view
		Window.draw(self.ToolBox)
		Window.view = Camera