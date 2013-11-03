from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200, 600), "Hivemind - Demo 2")

################################################

from sfml import View
from code.sfml_plus import Rectangle

class Camera(View, Rectangle):
# * May move move around the map (directional)
# WIP - May zoom in and out the map (smoothly)

	def __init__(self, window, args=None):
		View.__init__(self, args)
		self.size = window.window.size
		self.original_size = self.size #
		self.position = 0,0

	# POSITION
	@property
	def x(self):
		cx = self.center[0]
		w = self.size[0]
		return cx - (w/2)
	@x.setter
	def x(self, arg):
		x = self.x
		self.move(arg-x, 0)

	@property
	def y(self):
		cy = self.center[1]
		h = self.size[1]
		return cy - (h/2)
	@y.setter
	def y(self, arg):
		y = self.y
		self.move(0, arg-y)

	@property
	def w(self): return self.size.x
	@property
	def h(self): return self.size.y


	# ZOOM
	_zoom = float(1)
	
	@property
	def zoom(self): return self._zoom
	@zoom.setter
	def zoom(self, ratio):
		if ratio <= 0: return
		self._zoom = float(ratio)
		#
		w, h = self.original_size
		w /= ratio; h /= ratio
		self.size = w, h



################################################

from code.game import WorldMap
WorldMap = WorldMap(10,10)

Camera = Camera(window)

while window.is_open:
	if window.is_focused:

		if key.ENTER.pressed():
			pass

		##############
		amt = 10
		if key.A.held(): Camera.x -= amt
		if key.D.held(): Camera.x += amt
		if key.W.held(): Camera.y -= amt
		if key.S.held(): Camera.y += amt

		if key.PLUS.pressed(): Camera.zoom *= 2
		if key.MINUS.pressed(): Camera.zoom /= 2
		##############

	window.clear((255,220,0))
	window.view = Camera
	WorldMap.draw(window, Camera)
	window.display()