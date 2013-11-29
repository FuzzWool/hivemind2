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
		self._create_drawables()
		self._animation = self._animation(self)

	def write(self, msg):
		self.Text.write(msg)
		self._animation.open()

	def close(self):
		self._animation.close()

	def draw(self, target, states):
		self._create_box()
		self._animation.play()

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

	def _create_drawables(self): #init
		f = Font("speech")
		self.Text = Text(f)
		self.Box = RectangleShape((0,0))
		self.Box_shading = RectangleShape((0,0))


	def _create_box(self): #draw
		size = self.size
		position = self.position
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
		#
		Box_shading = RectangleShape((w,2))
		Box_shading.fill_color = Color(150,150,150)
		Box_shading.position = x,y
		#
		self.Box_shading = Box_shading


	class _animation(object):
	# * opens window
	# WIP - types text letter-by-letter
	# WIP - closes window

		def __init__(self, Speech): #Speech.init
			self._ = Speech
			self.Ay = Animation()
			self._init_text()

		def play(self): #Speech.draw (loop)
			self._play_openclose()
			self._play_text()


		###########
		# OPEN / CLOSE

		opening = True
		closing = False

		def open(self): #Speech.write
			self.opening = True
			self.closing = False
			

			self.Ay.speed = 0
			self.Ay.end = -10
			self.Ay.vel = -0.1
			self._.box_alpha = 0
			self.pro_y = 0
			#
			self._reset_text()
		
		def close(self): #Speech.close
			self.opening = False
			self.closing = True
			
			self.Ay.speed = 0
			self.Ay.end = +10
			self.Ay.vel = +0.1
			self._.box_alpha = 255
			self.pro_y = 0


		#

		def _play_openclose(self): #play
			Ay = self.Ay
			pro_y = self.pro_y

			#progress
			move = Ay.play(pro_y)
			self._.y += move

			if self.opening: self.box_alpha += (255/15)
			if self.closing:
				self.box_alpha -= (255/15)
				self.text_alpha -= (255/15)

			#stop
			self.pro_y += move
			if Ay.end == pro_y:
				self.opening = False
				self.stopped = False



		###########
		# TEXT

		def _init_text(self): #init
			self.letter_index = 0
			self.text_alpha = 0

		def _reset_text(self): #open
			self._init_text()

		def _play_text(self): #play
			if self.opening: return
			if self.closing: return

			i = self.letter_index
			letters = self._.Text.letters
			if i > len(letters)-1: return
			#
			letter = self._.Text.letters[i]
			amt = +100
			c = letter.color
			a = c.a + amt
			if a > 255: a = 255
			c.a = a
			letter.color = c
			#
			if a == 255:
				self.letter_index += 1



		###########
		# ALPHA

		_box_alpha = 255

		@property
		def box_alpha(self): return self._box_alpha
		@box_alpha.setter
		def box_alpha(self, a): #play
			if a > 255: a = 255
			if a < 0: a = 0
			self._box_alpha = a

			def update(Drawable):
				c = Drawable.fill_color; c.a = a
				Drawable.fill_color = c
				c = Drawable.outline_color; c.a = a
				Drawable.outline_color = c

			update(self._.Box)
			update(self._.Box_shading)


		_text_alpha = 255

		@property
		def text_alpha(self): return self._text_alpha
		@text_alpha.setter
		def text_alpha(self, a):
			if a > 255: a = 255
			if a < 0: a = 0
			self._text_alpha = a

			def update(Drawable):
				c = Drawable.color; c.a = a
				Drawable.color = c

			update(self._.Text)

#####################################

Speech = Speech()
Speech.write("HiveminD")
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