from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
##########################################

from code.sfml_plus import Rectangle
from code.sfml_plus import TweenRectangle
from sfml import RectangleShape, Color

class _UI(Rectangle):
# Communication


	### LOGIC
	# The parent controls the children's controls.

	def __init__(self):
		self.children = []

	def controls(self, Key, Mouse, Camera):
		for child in self.children:
			child.controls(Key, Mouse, Camera)

	def draw(self, Window):
		self._children_position()
		self._children_alpha()
		for child in self.children:
			child.draw(Window)


	### GRAPHICS
	# The parent moves and the children then follow.
	# Also, changes the children's alpha.

	old_pos = 0,0
	def _children_position(self): #draw
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		for child in self.children:
			child.x += x_move
			child.y += y_move
		self.old_pos = self.position

	alpha = 255
	def _children_alpha(self):
		for child in self.children:
			child.alpha = self.alpha


class Box(TweenRectangle, _UI):
# Graphics
# * A raised box with a shadow.
# Events
# * Fancily opens and closes.

	alpha = 255
	_alpha_move = 0

	##### EVENTS
	# Sets up movements and transparency for animation.

	def open(self):
		self.alpha = 0
		self._alpha_move = +30
		self.tween.y -= 20

	def close(self):
		self.alpha = 255
		self._alpha_move = -30
		self.tween.y += 20

	#

	def draw(self, Window):
		self._play()
		box = self.box()
		shadow = self.shadow()
		self._update_alpha(box,shadow)
		Window.draw(box)
		Window.draw(shadow)
		#
		_UI.draw(self, Window)

	####################


	##### GRAPHICS
	# Creates boxes each loop in order to position them.

	# w,h = 200,100
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
	# Saves an alpha, forces the graphics to use it.
	# The children refresh their positions to keep up.

	def __init__(self):
		_UI.__init__(self)
		TweenRectangle.__init__(self)
		self.size = 200,100

	def _play(self): #draw
		self.tween.play()

	def _update_alpha(self, box,shadow): #draw
		self._change_alpha()
		self._update(box,shadow)

	#

	def _change_alpha(self):
		a, amt = self.alpha, self._alpha_move
		if a + amt < 0: a = 0
		elif a + amt > 255: a = 255
		else: a += amt
		self.alpha = a

	def _update(self, box,shadow):
		a=self.alpha
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

box2 = Box()
box2.size = 75,75
box1.children.append(box2)

box3 = Box()
box3.size = 50,50
box2.children.append(box3)

box4 = Box()
box4.size = 25,25
box3.children.append(box4)

while Window.is_open:
	if Window.is_focused:

		if Key.ENTER.pressed():
			box1.tween.x -= 100

		if Key.BACKSPACE.pressed():
			box1.tween.x += 100

		# if Key.ENTER.pressed():
		# 	if box1.alpha == 255:
		# 		box1.close()
		# 	if box1.alpha == 0:
		# 		box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	box1.draw(Window)
	Window.display(Mouse)