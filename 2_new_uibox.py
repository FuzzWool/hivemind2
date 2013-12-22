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
	box_fill = Color.WHITE
	box_outline = Color.BLACK

	rise = 5
	@property
	def rise_offset(self): return self.rise-self.old_rise

	#

	old_rise = rise
	def box(self): #draw
		size = self.w, self.h+self.rise
		b = RectangleShape(size)
		b.position = self.x, self.y-self.rise_offset
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


##########################################
# BUTTONS

from code.sfml_plus import Font, Text

class Button(Box):
# State Handling
# 	* Hovering, Pressing, Selecting
# Graphics
# 	* Rises based on state.
# 	* Colored based on state.
#	* (Optional) contains text.

	w,h = 50,20

	def controls(self,Key, Mouse, Camera):
		self._hover(Mouse)
		self._select(Mouse)
		self._held(Mouse)
		self._color_states()
		Box.controls(self,Key,Mouse,Camera)

	def draw(self, Window):
		Box.draw(self, Window)
		self._draw_Text(Window)


	####################
	### STATE HANDLING

	hovered = False
	held = False
	selected = False

	def _hover(self, Mouse):
		self.hovered = Mouse.inside(self)

	def _held(self, Mouse):
		if Mouse.left.pressed():
			if self.hovered:
				self.held = True
				self.rise = 0
		elif not Mouse.left.held():
			self.held = False
			self.rise = self.old_rise

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
	# Create, pos/alpha, draw

	_Text = Text(Font("speech"))
	text = ""
	_text = text

	def _draw_Text(self, Window):
		#update text
		if self._text != self.text:
			self._Text.write(self.text)
		#color
		text = self._Text
		c=text.color;c.a=self.alpha;text.color=c
		#pos
		text.center = self.center
		text.y -= self.rise_offset
		#draw
		Window.draw(text)



####

class Cancel_Button(Button):
# Graphics - colors/text

	hovered_color = Color(255,150,150)
	held_color = Color.RED
	selected_color = Color.RED
	text = "Nah"

class Accept_Button(Button):
	hovered_color = Color(150,255,150)
	held_color = Color.GREEN
	selected_color = Color.GREEN
	text = "Sure"


##########################################
#SLIDERS

class Slider(_UI): #horizontal
# Graphics
# * A variable amount of lines spanning the width.

	w,h = 150,15
	lines = 5
	value = float(0) # to 100

	def __init__(self):
		_UI.__init__(self)
		self._create_Box()

	def controls(self, Key, Mouse, Camera):
		_UI.controls(self, Key, Mouse, Camera)
		self._Box_controls(Mouse)

	def draw(self, Window):
		self._create_baseLine()
		self._create_Lines()
		lines = self.Lines + [self.baseLine]
		for line in lines: Window.draw(line)
		#
		self._parent_Box()
		self.Box.draw(Window)
		#
		_UI.draw(self, Window)

	####################

	### GRAPHICS
	# Creates measurement lines and a box.
	# create, pos/alpha, draw
	baseLine = None
	Lines = []
	Box = None

	def _create_baseLine(self):
		self.baseLine = RectangleShape((self.w,0))
		self.baseLine.position = self.x, self.center[1]
		self.baseLine.outline_thickness = 1
		self.baseLine.outline_color = Color(0,0,0)

		#color
		b = self.baseLine
		c=b.outline_color;c.a=self.alpha;b.outline_color=c


	def _create_Lines(self):
		self.Lines = []

		for i in range(self.lines):
			w = float(self.w)/(self.lines-1)

			line = RectangleShape((0,self.h))
			x = self.x+(w*(i))
			line.position = x, self.y
			line.outline_thickness = 1
			line.outline_color = Color.BLACK

			#color
			c=line.outline_color;c.a=self.alpha
			line.outline_color=c

			self.Lines.append(line)

	def _create_Box(self):
		self.Box = Button()
		self.Box.text = " "
		self.Box.size = 20,self.h
		self.Box.x -= (self.Box.w/2)
		self.Box.y -= self.Box.rise

	def _parent_Box(self):

		#Follow parents' movement/alpha.
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		self.Box.x += x_move
		self.Box.y += y_move
		#
		self.Box.alpha = self.alpha

	### LOGIC
	
	def _Box_controls(self, Mouse):
		self.Box.controls(None, Mouse, None)
		#
		
		#Hold and drag: move the cursor.
		if self.Box.held:
			v = Mouse.x - self.x1
			if v < 0: v = 0
			if v > self.w: v = self.w

			self.Box.x += (self.x1-self.Box.center[0])+v
			self.value = (float(v)/self.w)*100

		# #Unpressed: go to nearest line.
		elif self.Box.selected:
			if self.lines > 2:
				w_chunk = float(self.w)/(self.lines-1)
				x = self.x
				while x < self.Box.x:
					x += w_chunk
				self.Box.center = x, self.Box.center[1]


##########################################


Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()
box1.center = Window.center

box2 = Accept_Button()
box2.x += box1.w - box2.w
box2.y += (box1.h - box2.h) - box2.rise
box1.children.append(box2)

box3 = Cancel_Button()
box3.x += box1.w - (box3.w*2)
box3.y += (box1.h - box3.h) - box3.rise
box1.children.append(box3)

slider = Slider()
slider.lines = 3
slider.center = box1.center
slider.x -= box1.x; slider.y -= box1.y + 30
box1.children.append(slider)

while Window.is_open:
	if Window.is_focused:

		# if Key.ENTER.pressed():
		# 	print slider.value

		if box2.selected:
			box1.close()

		if Key.ENTER.pressed():
			box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	box1.draw(Window)
	Window.display(Mouse)