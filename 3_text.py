from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Camera


Window = Window((1200,600), "Text Class")
Camera = Camera(Window)
Camera.zoom = 2
Camera.position = 0,0

#####################################


from sfml import Drawable
from code.sfml_plus import Rectangle
from code.sfml_plus.graphics import Font, Text
from sfml import Color
from sfml import RectangleShape
#
from code.sfml_plus import Animation


class Speech(Drawable, Rectangle):
# * write
# * position
# * alpha

# * fanciness:
#	boxes Text in a speech bubble.
# 	WIP - shows each letter one-by-one.
# 	WIP - opens/closes in a fancy way

	def __init__(self):
		Drawable.__init__(self)
		self._animation = self._animation(self)
		self._create_drawables()

	def write(self, msg):
		self.Text.write(msg)
		self._animation.bounce()

	def draw(self, target, states):
		self._animation.play()

		self._create_box()
		self._update_alpha()
		if self.Box:
			target.draw(self.Box)
			target.draw(self.Box_shading)
		target.draw(self.Text)


	#######
	# POSITION

	padding = 5

	@property
	def x(self): return self.Text.x - self.padding
	@property
	def y(self): return self.Text.y - self.padding
	@property
	def w(self): return self.Text.w + (self.padding*2)
	@property
	def h(self): return self.Text.h + (self.padding*2)+2

	@x.setter
	def x(self, x): self.Text.x = x + self.padding
	@y.setter
	def y(self, y): self.Text.y = y + self.padding
	# no w/h


	#######
	# DRAWABLES

	alpha = 255

	def _update_alpha(self): #draw
		if self.alpha > 255: self.alpha = 255
		a = self.alpha

		def update(Drawable):
			if type(Drawable) == Text:
				c = Drawable.color; c.a = a
				Drawable.color = c
			if type(Drawable) == RectangleShape:
				c = Drawable.fill_color; c.a = a
				Drawable.fill_color = c
				c = Drawable.outline_color; c.a = a
				Drawable.outline_color = c

		update(self.Text)
		update(self.Box)
		update(self.Box_shading)


	#

	def _create_drawables(self): #init
		f = Font("speech")
		self.Text = Text(f)
		self.Box = None
		self.Box_shading = None


	def _create_box(self): #draw
		size = self.size
		position = self.position
		a = self.alpha
		#
		Box = RectangleShape(size)
		Box.position = position
		Box.fill_color = Color(255,255,255)
		Box.outline_color = Color(0,0,0)
		Box.outline_thickness = 1
		#
		self.Box = Box
		#
		self._create_box_shading()

	def _create_box_shading(self): #_create_box
		w = self.w
		x,y = self.x, self.y2-2
		a = self.alpha
		#
		Box_shading = RectangleShape((w,2))
		Box_shading.fill_color = Color(150,150,150)
		Box_shading.position = x,y
		#
		self.Box_shading = Box_shading


	class _animation:
	# * opens window
	# WIP - types text letter-by-letter
	# WIP - closes window

		def __init__(self, Speech): #Speech.init
			self._ = Speech
			self.Ay = None

		def bounce(self): #Speech.write
			if not self.Ay:
				Ay = Animation()
				Ay.end = 0.1
				Ay.speed = -1.5
				Ay.vel = 0.2
				self.Ay = Ay
				self._.alpha = 0
				self.pro_y = 0

		def play(self): #Speech.draw (loop)
			if not self.Ay: return

			Ay = self.Ay
			pro_y = self.pro_y

			#progress
			move = Ay.play(pro_y)
			self._.y += move
			self._.alpha += (255/15)

			#stop
			self.pro_y += move
			if pro_y == Ay.end:
				self.Ay = None


#####################################

Speech = Speech()
Speech.write("Hello! My name is Sam.")
Speech.center = Camera.center

while Window.is_open:
	if Window.is_focused:

		if Key.ENTER.pressed():
			from random import randrange
			r = randrange(0,4)
			txt = [
				"HELLO EVERYONE. MY NAME IS SAM!",
				"I LIKE YOU. You like me. WE ARE HAPPY.",
				"Oh no! Its the police!",
				"Everyone! On the floor NOW."
				]
			Speech.write(txt[r])
			Speech.center = Camera.center

		if Key.A.pressed():
			Speech.alpha = 0
			print "A"

	Window.view = Camera
	Window.clear((100,100,100))
	Window.draw(Speech)
	Window.display()