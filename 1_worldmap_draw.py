from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200, 600), "Hivemind - Demo 2")

################################################

from sfml import View
from code.sfml_plus import Rectangle

class Camera(View, Rectangle):
# * May move move around
# * May zoom in and out

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

from code.sfml_plus import Animation


class AnimatedCamera(Camera):
	
	def __init__(self, *args):
		Camera.__init__(self, *args)
		#
		self.AZoom = Animation()
		self.zoom = float(self.zoom)
		self.smooth_zoom = float(self.zoom)

	@property
	def smooth_zoom(self): return self.AZoom.end
	@smooth_zoom.setter
	def smooth_zoom(self, zoom): self.AZoom.end = zoom

	def play(self):
		self._change_speed()
		self.zoom += self.AZoom.play(self.zoom)


	def _change_speed(self):
		# apply speed if the end hasn't been reached
		if self.zoom != self.smooth_zoom\
		and self.AZoom.speed != 0.05:
			self.AZoom.speed = 0.05

		# reverse speed if the end is the wrong direction
		if self.zoom < self.smooth_zoom:
			self.AZoom.speed = +abs(self.AZoom.speed)
		if self.zoom > self.smooth_zoom:
			self.AZoom.speed = -abs(self.AZoom.speed)


################################################

from code.game import WorldMap
WorldMap = WorldMap(4,4)

Camera = AnimatedCamera(window)

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

		if key.Q.pressed(): Camera.smooth_zoom /= 2
		if key.E.pressed(): Camera.smooth_zoom *= 2
		##############

	Camera.play()

	window.clear((255,220,0))
	window.view = Camera
	WorldMap.draw(window, Camera)
	window.display()