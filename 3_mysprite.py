from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200,600), "MySprite")

##############################################

from sfml import Sprite
from code.sfml_plus import Rectangle

class MySprite(Sprite, Rectangle):
# * Consistent with Rectangle's bindings.
# * Loads sub-classes.

	def __init__(self, *args):
		Sprite.__init__(self, *args)
		self.clip = clip(self)

	#Rectangle
	@property
	def x(self): return self.position.x
	@x.setter
	def x(self, x): self.position = x, self.y

	@property
	def y(self): return self.position.y
	@y.setter
	def y(self, y): self.position = self.x, y

	@property
	def w(self): return self.clip.w
	@property
	def h(self): return self.clip.h
	#

class clip:
	def __init__(self, MySprite):
		self._ = MySprite
		self.x, self.y = 0,0

	def set(self, *size):
		self.w, self.h = size

	def use(self, *position):
		self.x, self.y = position
		w, h = self.w, self.h
		x, y, w, h = x*w, y*h, w, h

		#flip
		if self.flipped_vertical: h = -h; y -= h
		if self.flipped_horizontal: w = -w; x -= w
		#

		self._.texture_rectangle = (x,y,w,h)

	# Flipping
	flipped_vertical = False
	flipped_horizontal = False

	def flip_vertical(self):
		self.flipped_vertical=not self.flipped_vertical
		self.use(self.x,self.y)

	def flip_horizontal(self):
		self.flipped_horizontal=not self.flipped_horizontal
		self.use(self.x,self.y)



# clip
# clip_animation
# interval

##############################################

from sfml import Texture

t = Texture.from_file("assets/tilesets/1.png")
sprite = MySprite(t)
sprite.position = 100,100

sprite.clip.set(25,25)
sprite.clip.use(1,0)


while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed():
			print "flipped vertical"
			sprite.clip.flip_horizontal()
			print sprite.position

	window.clear((255,220,0))
	window.draw(sprite)
	window.display()