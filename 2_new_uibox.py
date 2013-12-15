from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
##########################################

from code.sfml_plus import Rectangle
from code.sfml_plus import TweenRectangle
from sfml import RectangleShape, Color

class _UI(Rectangle):
# Communication

	x,y,w,h = 0,0,0,0
	graphics = []

	def controls(self, Key, Mouse, Camera):
		pass

	def draw(self, Window):
		pass


class Box(TweenRectangle, _UI):
# Graphics
# * A raised box with a shadow.
# Events
# * Fancily opens and closes.

	_alpha = 255
	_alpha_move = 0

	def open(self):
		self._alpha = 0
		self._alpha_move = +30
		self.tween.y -= 50

	def close(self):
		self._alpha = 255
		self._alpha_move = -30
		self.tween.y += 50

	#

	def draw(self, Window):
		box = self.box()
		shadow = self.shadow()
		self._play(box, shadow)
		Window.draw(box)
		Window.draw(shadow)

	####################


	##### GRAPHICS
	w,h = 200,100
	rise = 5

	def box(self): #draw
		size = self.w, self.h+self.rise
		b = RectangleShape(size)
		b.position = self.position
		b.outline_thickness = 1
		b.outline_color = Color.BLACK
		return b

	def shadow(self):
		w,h = self.size
		b = RectangleShape((w,self.rise))
		b.position = self.x, self.y2
		b.fill_color = Color(200,200,200)
		return b


	##### ANIMATION
	def __init__(self):
		TweenRectangle.__init__(self)

	def _play(self, box,shadow):
		self.tween.play()
		self._change_alpha()
		self._update(box,shadow)

	#

	def _change_alpha(self):
		a, amt = self._alpha, self._alpha_move
		if a + amt < 0: a = 0
		elif a + amt > 255: a = 255
		else: a += amt
		self._alpha = a

	def _update(self, box,shadow):
		a=self._alpha
		c=box.fill_color;c.a=a;box.fill_color=c
		c=box.outline_color;c.a=a;box.outline_color=c
		c=shadow.fill_color;c.a=a;shadow.fill_color=c


class Button(Box):
# State Handling
	pass


##########################################
Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()
box1.center = Window.center
box1.open()

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed():
			if box1._alpha == 255:
				box1.close()
			if box1._alpha == 0:
				box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	box1.draw(Window)
	Window.display(Mouse)