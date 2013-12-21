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

	w,h = 200,100
	rise = 5
	box_fill = Color.WHITE
	box_outline = Color.BLACK

	#

	old_rise = rise
	def box(self): #draw
		rise_dist = self.rise-self.old_rise
		size = self.w, self.h+self.rise
		b = RectangleShape(size)
		b.position = self.x, self.y-rise_dist
		b.outline_thickness = 1
		b.outline_color = self.box_outline
		b.fill_color = self.box_fill
		return b

	def shadow(self): #draw
		w,h = self.size
		b = RectangleShape((w,self.rise))
		b.position = self.x, self.y2
		b.fill_color = Color(0,0,0,255)
		return b


	##### ANIMATION
	# Saves an alpha, forces the graphics to use it.
	# The children refresh their positions to keep up.

	def __init__(self):
		_UI.__init__(self)
		TweenRectangle.__init__(self)

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
		c=shadow.fill_color;c.a=a/4;shadow.fill_color=c


from code.sfml_plus import Font, Text

class Button(Box):
# State Handling
# 	* Hovering, Pressing, Selecting
# Graphics
# 	* Rises based on state.
# 	* Colored based on state.
#	* (Optional) contains text.

	w,h = 50,20

	def controls(self,*args):
		self._hover(Mouse)
		self._select(Mouse)
		self._held(Mouse)
		self._color_states()
		Box.controls(self,*args)


	### STATE HANDLING

	hovered = False
	def _hover(self, Mouse):
		self.hovered = Mouse.inside(self)

	held = False
	def _held(self, Mouse):
		if Mouse.left.pressed():
			if self.hovered:
				self.held = True
				self.rise = 0
		elif not Mouse.left.held():
			self.held = False
			self.rise = self.old_rise

	selected = False
	def _select(self, Mouse):
		self.selected = False
		if not Mouse.left.held():
			if self.held:
				self.selected = True


	### COLORING

	box_fill = Color(240,240,240)
	old_fill = box_fill
	hovered_color = Color(255,255,255)
	held_color = hovered_color
	selected_color = hovered_color

	def _color_states(self):
		self.box_fill = self.old_fill
		if self.hovered:
			self.box_fill = self.hovered_color
		if self.held:
			self.box_fill = self.held_color
		if self.selected:
			self.box_fill = self.selected_color


	### TEXT (Optional)
	# Create, move, draw

	graphics = []
	_text = Text(Font("speech"))

	@property
	def text(self): return self._text.string
	@text.setter
	def text(self, t):
		self._text.write(t)


	# def draw(self, Window):
	# 	self._text.center = self.center
	# 	self.graphics.append(self._text)
	# 	Box.draw(self, Window)



####

class Close_Button(Button):
# Graphics
# * Red state colors.

	hovered_color = Color(255,150,150)
	held_color = Color.RED
	selected_color = Color.RED



##########################################
Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()
box1.center = Window.center

box2 = Close_Button()
box2.x += box1.w - box2.w
box2.y -= box2.rise
box2.text = "hello"
box1.children.append(box2)

while Window.is_open:
	if Window.is_focused:

		# if Key.ENTER.pressed():
		# 	box1.tween.x -= 100

		# if Key.BACKSPACE.pressed():
		# 	box1.tween.x += 100

		if box2.selected:
			box1.close()

		if Key.ENTER.pressed():
			box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	box1.draw(Window)
	Window.display(Mouse)