from code.sfml_plus import Window
from code.sfml_plus import Key

#######################################

from code.sfml_plus import Rectangle
from sfml import RectangleShape
from sfml import Color
from code.sfml_plus import Animation
from code.sfml_plus.graphics.animation import Magnet


class _UIBox(Rectangle):
	
	def _create_box(self): #draw
	#Updates the box to the new points every loop.
		x,y = self.position
		w,h = self.size
		#
		Box = RectangleShape((w,h))
		Box.position = x,y
		Box.outline_color = Color(0,0,0)
		Box.outline_thickness = 1
		#
		self.Box = Box


	_end_alpha = 255 #open/close
	_alpha = 255
	def _play_alpha(self): #draw
	#Change the alpha of all of the graphics.
		_alpha = self._alpha
		_end_alpha = self._end_alpha
		amt = 25
		#
		if _alpha < _end_alpha:
			if _alpha+amt > 255: _alpha = 255
			else: _alpha += amt
		if _alpha > _end_alpha:
			if _alpha-amt < 0: _alpha = 0
			else: _alpha -= amt
		#
		def update(G):
			if type(G) == RectangleShape:
				c = G.fill_color; c.a = _alpha
				G.fill_color = c
				c = G.outline_color; c.a = _alpha
				G.outline_color = c

		self._alpha = _alpha
		update(self.Box)





	### POSITION
	# * position: forces smooth position with it

	_x, _y = 0,0

	@property
	def x(self): return self._x
	@property
	def y(self): return self._y

	@x.setter
	def x(self, x):
			self._x = x
			self.Smooth.x = x

	@y.setter
	def y(self, y):
			self._y = y
			self.Smooth.y = y


	class Smooth(Rectangle):
	# * Sets position for the Rectangle to animate to.

		_x,_y = 0,0

		def __init__(self, UIBox): #_.init
			self._ = UIBox
			self.points = self._.points

			self.animation_x = Animation()
			self.animation_y = Animation()
			self.animation_x.mode = Magnet
			self.animation_y.mode = Magnet

		def play(self): #_.draw

			self.animation_x.end = self.x
			self.animation_y.end = self.y

			speed_x = abs((self.x-self._.x)/5)
			speed_y = abs((self.y-self._.y)/5)
			self.animation_x.speed = speed_x
			self.animation_y.speed = speed_y

			old_x = self.x
			old_y = self.y
			self._.x += self.animation_x.play(self._.x)
			self._.y += self.animation_y.play(self._.y)
			self.x = old_x
			self.y = old_y


class _UIDropdown:
	pass


###############

class UIBox(_UIBox):

	def __init__(self):
		self.Smooth = self.Smooth(self)

	#

	def controls(self):
		pass

	def draw(self, Window):
		self._create_box()
		self._play_alpha()
		self.Smooth.play()
		Window.draw(self.Box)

	#

	def open(self):
		amt = 20
		self.y += amt
		self.Smooth.y = self.y - amt
		self._alpha = 0
		self._end_alpha = 255

	def close(self):
		amt = 20
		self.Smooth.y = self.y + amt
		self._alpha = 255
		self._end_alpha = 0

	#####

class UIDropdown:

	def controls(self):
		pass

	def draw(self):
		pass


#######################################


Window = Window((1200,600), "UI Box (Tile)")

UIBox = UIBox()
UIBox.size = 100,100
UIBox.open()

while Window.is_open:
	if Window.is_focused:

		if Key.ENTER.pressed(): UIBox.open()
		if Key.BACKSPACE.pressed(): UIBox.close()

	Window.clear((255,220,0))
	UIBox.draw(Window)
	Window.display()