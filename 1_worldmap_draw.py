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
from code.sfml_plus.animation import Magnet

class SmoothCamera(Camera):
	
	def __init__(self, *args):
		Camera.__init__(self, *args)
		self.smooth = Smooth(self)


class Smooth(Rectangle):
# WIP - Smoothly moves around directionally.
# * Smoothly zooms in.
	def __init__(self, Camera):
		self._ = Camera
		self._pos_init()
		self._zoom_init()

	def play(self):
		self._pos_play()
		self._zoom_play()


	#### POS

	@property
	def x(self): return self.XA.end - (self.w/2)
	@x.setter
	def x(self, arg): self.XA.end = arg + (self.w/2)

	@property
	def y(self): return self.YA.end - (self.h/2)
	@y.setter
	def y(self, arg): self.YA.end = arg + (self.h/2)

	@property
	def w(self): return self._.w
	@property
	def h(self): return self._.h


	def _pos_init(self): #init
		#x
		self.XA = Animation()
		self.XA.mode = Magnet
		self.x = 0
		#y
		self.YA = Animation()
		self.YA.mode = Magnet
		self.y = 0

	def _pos_play(self): #play
		d = 5
		current_x, current_y = self._.center
		end_x, end_y = self.center

		#
		self.XA.speed=int(abs(current_x - self.XA.end)/d)
		current_x += self.XA.play(current_x)

		self.YA.speed=int(abs(current_y - self.YA.end)/d)
		current_y += self.YA.play(current_y)
		#

		self._.center = current_x, current_y


	#### ZOOM

	@property
	def zoom(self): return self.ZoomA.end
	@zoom.setter
	def zoom(self, arg): self.ZoomA.end = arg


	def _zoom_init(self): #init
		self.ZoomA = Animation()
		self.ZoomA.mode = Magnet
		self.zoom = self._.zoom

	def _zoom_play(self): #play

		self.ZoomA.speed = 0.1
		self._.zoom += self.ZoomA.play(self._.zoom)


################################################

from code.game import WorldMap
WorldMap = WorldMap(4,4)

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