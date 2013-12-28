from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
##########################################

from code.sfml_plus.ui import _UI, Button
from sfml import RectangleShape, Color

from code.sfml_plus.ui import Box
from code.sfml_plus import Rectangle

class Slider(_UI): #horizontal
# Logic
# * A box goes back and forth a line, determining value.
# * A line amount may be specified.
#   The cursor automatically snaps to inbetween lines.
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

	def draw(self, target, states):
		self._create_baseLine()
		self._create_Lines()
		lines = self.Lines + [self.baseLine]
		for line in lines: target.draw(line)
		#
		self._parent_Box()
		target.draw(self.Box)
		#
		_UI.draw(self, target, states)

	####################

	### GRAPHICS
	# Creates measurement lines and a box.
	# create, pos/alpha, draw
	baseLine = None
	Lines = []
	Box = None
	using = "x"

	def _create_baseLine(self):

		if self.using == "x":
			self.baseLine = RectangleShape((self.w,0))
			self.baseLine.position = self.x,self.center[1]
		if self.using == "y":
			self.baseLine = RectangleShape((0,self.h))
			self.baseLine.position = self.center[0],self.y

		self.baseLine.outline_thickness = 1
		self.baseLine.outline_color = Color(0,0,0)

		#color
		b = self.baseLine
		c=b.outline_color;c.a=self.alpha;b.outline_color=c


	def _create_Lines(self):
		self.Lines = []

		for i in range(self.lines):

			if self.using == "x":
				w = float(self.w)/(self.lines-1)
				line = RectangleShape((0,self.h))
				x = self.x+(w*(i))
				line.position = x, self.y
			
			if self.using == "y":
				h = float(self.h)/(self.lines-1)
				line = RectangleShape((self.w,0))
				y = self.y+(h*(i))
				line.position = self.x, y

			line.outline_thickness = 1
			line.outline_color = Color.BLACK

			#color
			c=line.outline_color;c.a=self.alpha
			line.outline_color=c

			self.Lines.append(line)


	### BOX
	move_x, move_y = None, None

	def _create_Box(self):
		self.Box = Button()
		self.Box.text = " "

		if self.using == "x":
			self.Box.size = 20,self.h
			self.Box.x -= (self.Box.w/2)
			self.Box.y -= self.Box.rise
		if self.using == "y":
			self.Box.size = self.w,20
			self.Box.y -= (self.Box.h/2)
			self.Box.y -= self.Box.rise

	def _Box_controls(self, Mouse):
		self.Box.controls(None, Mouse, None)
		#
		
		#Hold and drag: move the cursor.
		if self.Box.held:

			if self.using == "x":
				v = Mouse.x - self.x1
				if v < 0: v = 0
				if v > self.w: v = self.w

				self.move_x += (self.x1-self.Box.center[0])+v
				self.value = (float(v)/self.w)*100

			if self.using == "y":
				v = Mouse.y - self.y1
				if v < 0: v = 0
				if v > self.h: v = self.h

				self.move_y += (self.y1-self.Box.center[1])+v
				self.value = (float(v)/self.h)*100

		#Unpressed: go to nearest line.
		elif self.Box.selected:
			if self.lines > 2:

				if self.using == "x":
					w_chunk = float(self.w)/(self.lines-1)
					x = self.x
					midpoint = (w_chunk/2)-(self.Box.w/2)
					while x + midpoint < self.Box.x:
						x += w_chunk
					self.Box.tween.x = x-(self.Box.w/2)
				
				if self.using == "y":
					h_chunk = float(self.h)/(self.lines-1)
					y = self.y
					midpoint = (h_chunk/2)-(self.Box.h/2)
					while y + midpoint < self.Box.y:
						y += h_chunk
					self.Box.tween.y = y-(self.Box.h/2)


	def _parent_Box(self):

		#Parent Movements
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		if x_move: self.Box.x += x_move
		if y_move: self.Box.y += y_move

		#Parent Alpha
		self.Box.alpha = self.alpha

		#Control Movements
		bounded = bool(self.lines <= 2)

		if self.move_x != 0 and self.using == "x":
			if self.move_x == None: self.move_x = 0
			self.Box.x += self.move_x
			if bounded:
				if self.Box.x1 < self.x1: self.Box.x = self.x1
				if self.Box.x2 > self.x2: self.Box.x = self.x2-self.Box.w

		if self.move_y != 0 and self.using == "y":
			if self.move_y == None: self.move_y = 0
			self.Box.y += self.move_y
			if bounded:
				if self.Box.y1 < self.y1: self.Box.y = self.y1
				if self.Box.y2 > self.y2: self.Box.y = self.y2-self.Box.h
				self.Box.y += self.Box.rise_offset

		self.move_x, self.move_y = 0,0



class Horizontal_Slider(Slider):
	using = "x"
	w,h = 150,15

class Vertical_Slider(Slider):
	using = "y"
	w,h = 15,150


##########################################

from code.sfml_plus.ui import _UI
from code.sfml_plus.ui import MaskBox

class SliderBox(_UI):
# A Slider controls a Maskbox's contents.

	#################################
	# PUBLIC

	def __init__(self):
		_UI.__init__(self)
		self._create_Box()
		self._create_Slider()
		self._update_rectangle()

	def controls(self, Key, Mouse, Camera):
		_UI.controls(self, Key, Mouse, Camera)
		self.Slider.controls(Key, Mouse, Camera)
		self.Box.controls(Key, Mouse, Camera)

	def draw(self, target, states):
		self._update_graphics()
		_UI.draw(self, target, states)
		self._resize_Slider()
		target.draw(self.Box)
		target.draw(self.Slider)

	#################################
	# PRIVATE

	def _create_Box(self):
		self.Box = MaskBox()

	def _create_Slider(self):
		self.Slider = Vertical_Slider()
		self.Slider.x += self.Box.w + (self.Slider.w/2)
		self.Slider.h = self.Box.h-1
		self.Slider.lines = 2

	def _update_rectangle(self):
		self.w = self.Slider.x2 - self.Box.x1
		self.h = self.Box.h

	def _update_graphics(self): #draw
		#alpha
		self.Box.alpha = self.alpha
		self.Slider.alpha = self.alpha
		#move
		move_x = self.x - self.old_pos[0]
		move_y = self.y - self.old_pos[1]
		self.Box.x += move_x; self.Box.y += move_y
		self.Slider.x += move_x; self.Slider.y += move_y

	old_children_len = 0
	def _resize_Slider(self): #draw)
		if self.old_children_len != len(self.Box.children):
			ratio = float(self.Box.offset.h) / float(self.Box.h)
			self.Slider.Box.h = (self.Slider.h/ratio)

		self.old_children_len = len(self.Box.children)

##########################################

from code.sfml_plus.ui import Box
from code.sfml_plus.ui import Accept_Button, Cancel_Button
# from code.sfml_plus.ui import Slider

Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()
box1.w += 100; box1.h += 100
box1.center = Window.center

box2 = Accept_Button()
box2.x += box1.w - box2.w
box2.y += (box1.h - box2.h) - box2.rise
box1.children.append(box2)

# box3 = Cancel_Button()
# box3.x += box1.w - (box3.w*2)
# box3.y += (box1.h - box3.h) - box3.rise
# box1.children.append(box3)

#

sliderbox = SliderBox()
sliderbox.x += (box1.w/2) - (sliderbox.w/2)
sliderbox.y += (box1.h/2) - (sliderbox.h/2)
sliderbox.y -= 20
box1.children.append(sliderbox)

sbox1 = Accept_Button()
sbox1.x += 5; sbox1.y += 1000
sliderbox.Box.children.append(sbox1)

##########################################

while Window.is_open:
	if Window.is_focused:

		if box2.selected\
		or Key.BACKSPACE.pressed():
			box1.close()

		if Key.ENTER.pressed():
			box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display(Mouse)