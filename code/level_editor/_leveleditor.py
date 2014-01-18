from background import Background
from toolbox import ToolBox

class LevelEditor:
# * Contains a background.
# * Handles Camera controls.

	#################################
	# PUBLIC

	def __init__(self, window):
		self.Background = Background(window)
		self.ToolBox = ToolBox(*window.size)


	def camera_controls(self, Key, Mouse, Camera):
		Camera.smooth.speed = 3

		if Key.L_CTRL.held(): return

		#Move (per Room)
		if Key.LEFT.pressed(): Camera.smooth.room_x -= 1
		if Key.RIGHT.pressed(): Camera.smooth.room_x += 1
		if Key.UP.pressed(): Camera.smooth.room_y -= 1
		if Key.DOWN.pressed(): Camera.smooth.room_y += 1

		#Move (per Tile)
		amt = 25
		if Key.A.held(): Camera.smooth.x -= amt
		if Key.D.held(): Camera.smooth.x += amt
		if Key.W.held(): Camera.smooth.y -= amt
		if Key.S.held(): Camera.smooth.y += amt

		#Zoom (Toggle)
		if Key.E.pressed():
			if   Camera.smooth.zoom == 1: Camera.smooth.zoom = 2
			elif Camera.smooth.zoom == 2: Camera.smooth.zoom = 1


	def controls(self, Key, Mouse, Camera):
		#toolbox
		self.ToolBox.controls(Key, Mouse, Camera)
		if Key.TAB.pressed(): self.ToolBox.toggle()

		self.Key, self.Mouse, self.Camera = Key, Mouse, Camera

	def add_controls(self, WorldMap):
		self.ToolBox.add_controls(WorldMap)

		# Toggle grid.
		if self.Key.Q.pressed():
			WorldMap.enable_grid = not WorldMap.enable_grid

		# Saving/Loading
		if self.Key.L_CTRL.held():
			if self.Key.S.pressed():
				self._save(WorldMap)
			if self.Key.O.pressed():
				self._load(WorldMap)


	#

	def draw_background(self, Window, Camera):
		self.Background.draw(Window, Camera)

	def draw_objects(self, Window, Camera):
		Window.view = Window.default_view
		self.ToolBox.static_draw(Window, None)
		Window.view = Camera
		self.ToolBox.normal_draw(Window, None)


	#################################
	# PRIVATE
	# * WorldMap saving/loading.

	_map_name = "map1"

	def _save(self, WorldMap):
		WorldMap.save(self._map_name)

	def _load(self, WorldMap):
		WorldMap.load(self._map_name)