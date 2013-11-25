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

class Speech(Drawable, Rectangle):
# * write
# * position

# * fanciness:
#	boxes Text in a speech bubble.
# 	WIP - shows each letter one-by-one.
# 	WIP - opens/closes in a fancy way

	def write(self, msg):
		self.Text.write(msg)

	def draw(self, target, states):
		self._create_box()
		if self.Box:
			target.draw(self.Box)
			target.draw(self.Box_shading)
		target.draw(self.Text)


	#######

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

	def __init__(self):
		Drawable.__init__(self)
		self._create_drawables()

	def _create_drawables(self): #init
		f = Font("speech")
		self.Text = Text(f)
		self.Box = None

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


#####################################

Speech = Speech()
Speech.write("Hello! My name is Sam.")
Speech.center = Camera.center

while Window.is_open:
	if Window.is_focused:

		if Key.ENTER.pressed():
			pass

	Window.view = Camera
	Window.clear((100,100,100))
	Window.draw(Speech)
	Window.display()