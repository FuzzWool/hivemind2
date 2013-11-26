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
# 	opens/closes in a fancy way.
# 	WIP - shows each letter one-by-one.

	def __init__(self):
		Drawable.__init__(self)
		self._animation = self._animation(self)
		self._create_drawables()

	def write(self, msg):
		self.Text.write(msg)
		self._animation.open()

	def close(self):
		self._animation.close()

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
		if self.alpha < 0: self.alpha = 0
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

		opening = True
		closing = False

		def open(self): #Speech.write
			self.opening = True
			self.closing = False
			

			self.Ay.speed = 0
			self.Ay.end = -10
			self.Ay.vel = -0.1
			self._.alpha = 0
			self.pro_y = 0
		
		def close(self): #Speech.close
			self.opening = False
			self.closing = True
			
			self.Ay.speed = 0
			self.Ay.end = +10
			self.Ay.vel = +0.1
			self._.alpha = 255
			self.pro_y = 0

		#

		def __init__(self, Speech): #Speech.init
			self._ = Speech
			self.Ay = Animation()


		def play(self): #Speech.draw (loop)

			Ay = self.Ay
			pro_y = self.pro_y

			#progress
			move = Ay.play(pro_y)
			self._.y += move

			if self.opening: self._.alpha += (255/15)
			if self.closing: self._.alpha -= (255/15)

			#stop
			self.pro_y += move


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

		if Key.BACKSPACE.pressed():
			Speech.close()

	Window.view = Camera
	Window.clear((100,100,100))
	Window.draw(Speech)
	Window.display()