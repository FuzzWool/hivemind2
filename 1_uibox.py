from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
##########################################

from code.sfml_plus.ui import _UI, Button
from sfml import RectangleShape, Color

from code.sfml_plus.ui import Box

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

	def _parent_Box(self):

		#Follow parents' movement/alpha.
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		if x_move: self.Box.x += x_move
		if y_move: self.Box.y += y_move
		#
		self.Box.alpha = self.alpha

	### LOGIC
	
	def _Box_controls(self, Mouse):
		self.Box.controls(None, Mouse, None)
		#
		
		#Hold and drag: move the cursor.
		if self.Box.held:

			if self.using == "x":
				v = Mouse.x - self.x1
				if v < 0: v = 0
				if v > self.w: v = self.w

				self.Box.x \
				+= (self.x1-self.Box.center[0])+v
				self.value = (float(v)/self.w)*100

			if self.using == "y":
				v = Mouse.y - self.y1
				if v < 0: v = 0
				if v > self.h: v = self.h

				self.Box.y \
				+= (self.y1-self.Box.center[1])+v
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


class Horizontal_Slider(Slider):
	using = "x"
	w,h = 150,15

class Vertical_Slider(Slider):
	using = "y"
	w,h = 15,150



class SliderBox(_UI):
	w = Box.w + Vertical_Slider.w
	h = Box.h

	def __init__(self):
		_UI.__init__(self)
		self._create_Box()
		self._create_Slider()

	def draw(self, Window):
		_UI.draw(self, Window)

	############################
	# GRAPHICS
	# Box, Slider

	def _create_Box(self):
		self.Box = Box()
		self.Box.box_fill = Color(200,200,200)
		self.children.append(self.Box)

	def _create_Slider(self):
		self.Slider = Vertical_Slider()
		self.Slider.lines = 2
		self.Slider.h = self.h
		self.Slider.x += self.w
		self.children.append(self.Slider)


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

box3 = Cancel_Button()
box3.x += box1.w - (box3.w*2)
box3.y += (box1.h - box3.h) - box3.rise
box1.children.append(box3)

sliderbox = SliderBox()
sliderbox.center = box1.center
sliderbox.x -= box1.x; sliderbox.y -= box1.y
sliderbox.y -= 15
box1.children.append(sliderbox)

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
	box1.draw(Window)
	Window.display(Mouse)