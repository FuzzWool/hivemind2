from code.sfml_plus import Window
from code.sfml_plus import Key

##############################

from sfml import RectangleShape
from sfml import Color
from code.sfml_plus import Animation
from code.sfml_plus.animation import Animation, Magnet
from code.sfml_plus import Rectangle

class UIBox(Rectangle):
# * May move around in block or .Smooth movements.
# WIP - Opens from nothingness.
# WIP - Closes to nothingness.

	def __init__(self):
		self.position = 300,300
		self.size = 100,100
		self.Smooth = self.Smooth(self)

	def draw(self, Window):
		self._create_rectangle()
		self.Smooth.play()
		Window.draw(self.rectangle)


	def _create_rectangle(self): #draw
		rectangle = RectangleShape(self.size)
		rectangle.position = self.position
		rectangle.outline_color = Color.BLACK
		rectangle.outline_thickness = 5
		self.rectangle = rectangle


	### RECTANGLE
	# * position: forces smooth position with it
	# * resize: centers with extension

	_x, _y, _w, _h = 0,0,0,0

	@property
	def x(self): return self._x
	@property
	def y(self): return self._y
	@property
	def w(self): return self._w
	@property
	def h(self): return self._h

	@x.setter
	def x(self, x):
		self._x = x
		self.Smooth.x = x

	@y.setter
	def y(self, y):
		self._y = y
		self.Smooth.y = y

	@w.setter
	def w(self, w):
		old_center = self.center
		self._w = w
		self.center = old_center

	@h.setter
	def h(self, h):
		old_center = self.center
		self._h = h
		self.center = old_center



	###

	class Smooth(Rectangle):
	# * Sets position for the Rectangle to animate to.

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


##############################

Window = Window((1200,600), "Untitled")
UIBox = UIBox()

while Window.is_open:
	if Window.is_focused:

		#move rectangle
		amt = 200
		if Key.A.pressed(): UIBox.Smooth.x -= amt
		if Key.D.pressed(): UIBox.Smooth.x += amt
		if Key.W.pressed(): UIBox.Smooth.y -= amt
		if Key.S.pressed(): UIBox.Smooth.y += amt


	Window.clear((255,220,0))
	UIBox.draw(Window)
	Window.display()