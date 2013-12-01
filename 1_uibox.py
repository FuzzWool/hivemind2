from code.sfml_plus import Window
from code.sfml_plus import Key

#######################################

from code.sfml_plus import Rectangle
from sfml import RectangleShape
from sfml import Color
from code.sfml_plus import Animation
from code.sfml_plus.graphics.animation import Magnet
from code.sfml_plus import Mouse

class _UIBox(Rectangle):
	
	### GRAPHICS

	def _create_box(self): #draw
		x,y = self.position
		w,h = self.size
		#
		Box = RectangleShape((w,h))
		Box.position = x,y
		Box.outline_color = Color(0,0,0)
		Box.outline_thickness = 1
		#
		self.Box = Box


	_end_alpha = 255 #open/close
	_alpha = 255
	def _play_alpha(self): #draw
	#Change the alpha of all of the graphics.
		_alpha = self._alpha
		_end_alpha = self._end_alpha
		amt = 25
		#
		if _alpha < _end_alpha:
			if _alpha+amt > 255: _alpha = 255
			else: _alpha += amt
		if _alpha > _end_alpha:
			if _alpha-amt < 0: _alpha = 0
			else: _alpha -= amt
		#

		def update(G):

			if type(G) == RectangleShape:
				c = G.fill_color; c.a = _alpha
				G.fill_color = c
				c = G.outline_color; c.a = _alpha
				G.outline_color = c

			if type(G) == Text:
				c = G.color; c.a = _alpha
				G.color = c

		self._alpha = _alpha
		update(self.Box)
		for UI in self.UIs:
			for graphic in UI.graphics:
				update(graphic)


	### POSITION
	# * position: forces smooth position with it

	_x, _y = 0,0

	@property
	def x(self): return self._x
	@property
	def y(self): return self._y

	@x.setter
	def x(self, x):
		move = x - self._x
		for UI in self.UIs:
			UI.x += move

		self._x = x
		self.Smooth.x = x

	@y.setter
	def y(self, y):
		move = y - self._y
		for UI in self.UIs:
			UI.y += move

		self._y = y
		self.Smooth.y = y


	class Smooth(Rectangle):
	# * Sets position for the Rectangle to animate to.

		_x,_y = 0,0

		def __init__(self, UIBox): #_.init
			self._ = UIBox
			self.points = self._.points

			self.animation_x = Animation()
			self.animation_y = Animation()
			self.animation_x.mode = Magnet
			self.animation_y.mode = Magnet

		def play(self): #_.draw

			self.animation_x.end = self.x
			self.animation_y.end = self.y

			speed_x = abs((self.x-self._.x)/5)
			speed_y = abs((self.y-self._.y)/5)
			self.animation_x.speed = speed_x
			self.animation_y.speed = speed_y

			old_x = self.x
			old_y = self.y
			self._.x += self.animation_x.play(self._.x)
			self._.y += self.animation_y.play(self._.y)
			self.x = old_x
			self.y = old_y



###############

class UIBox(_UIBox):

	def __init__(self):
		self.Smooth = self.Smooth(self)

	#

	UIs = []
	def add(self, UI):
		self.UIs.append(UI)

	#

	def controls(self, *args):
		for UI in self.UIs:
			UI.controls(*args)

	def draw(self, Window):
		self._create_box()
		self._play_alpha()
		self.Smooth.play()
		Window.draw(self.Box)

		for UI in self.UIs:
			UI.draw(Window)

	###

	def open(self):
		amt = 20
		self.y += amt
		self.Smooth.y = self.y - amt
		self._alpha = 0
		self._end_alpha = 255

	def close(self):
		amt = 20
		self.Smooth.y = self.y + amt
		self._alpha = 255
		self._end_alpha = 0


######

class _UI(Rectangle):

	graphics = []

	def controls(self, Key, Mouse, Camera):
		pass

	def draw(self, Window):
		pass


from code.sfml_plus.graphics import Font, Text

class Dropdown(_UI):
# G: Draws cells.
# L: Forwards mouse events to cells.
# WIP - L: Opens list cells as their own dropdowns.

	w,h = 100,20
	cell_input = []

	def __init__(self, cell_input):
		self.cell_input = cell_input
		self._create_cells()

	def controls(self, Key, Mouse, Camera):
		self._opening_check(Mouse)
		self.create_graphics()

	def draw(self, Window):
		self._draw_cells(Window)

	################################################


	### CELLS
	#

	def _create_cells(self): #init
		self.cells = []
		#
		for cell_i in self.cell_input:
			if type(cell_i) == str:
				cell = Cell(cell_i)
			if type(cell_i) == list:
				cell = Dropdown(cell_i)
			
			self.cells.append(cell)

	def create_graphics(self): #controls
		
		x,y = self.position
		for cell in self.cells:
			cell.position = x,y
			cell.create_graphics()
			y += cell.h

		#refresh graphics
		self.graphics = []
		for cell in self.cells:
			for graphic in cell.return_graphics():
				self.graphics.append(graphic)


	def return_graphics(self): #controls
	# (Only when treated as a cell)

		r_graphics = []
		for cell in self.cells:
			for graphic in cell.return_graphics():
				r_graphics.append(graphic)
		return r_graphics


	def _draw_cells(self, Window): #draw

		for cell in self.cells:
			cell.draw(Window)


	### CONTROLS
	#

	opened = False

	def _opening_check(self, Mouse): #controls
		
		# if Mouse.left.pressed():
		# 	if Mouse.inside(self):
		# 		self.opened = not self.opened
		# 	else:
		# 		self.opened = False

		#

		for cell in self.cells:
			cell.controls(None, Mouse, None)

#



class Cell(Rectangle):
# WIP - G: Creates a box. Holds text.
# WIP - L: May be selected.

	text = "untitled_cell"
	selected = False
	highlighted = False

	def __init__(self, text): #dropdown.init
		self.text = text

	#

	def controls(self, Key, Mouse, Camera):
		self.highlighted = Mouse.inside(self)

		if Mouse.left.pressed():
			self.selected = Mouse.inside(self)

	#

	def create_graphics(self): #dropdown.controls
		self._create_box()
		self._create_gtext()

	def return_graphics(self): #dropdown.controls
		return self.box, self.gtext

	def draw(self, Window): #dropdown.draw
		Window.draw(self.box)
		Window.draw(self.gtext)

	#############################################

	### GRAPHICS

	x,y,w,h = 0,0,100,20
	font = Font("speech")

	def _create_box(self):
		x,y = self.position
		w,h = self.size
		highlighted = self.highlighted
		selected = self.selected
		#
		box = RectangleShape((w,h))
		box.position = x,y
		box.outline_color = Color.BLACK
		box.outline_thickness = 1

		if highlighted: box.fill_color = Color(255,255,20)
		if selected: box.fill_color = Color(200,200,150)
		
		#
		self.box = box

	def _create_gtext(self):
		x,y = self.position
		x += 3; y += 3
		text = self.text
		#
		gtext = Text(self.font)
		gtext.write(text)
		gtext.position = x,y
		#
		self.gtext = gtext
	#



#######################################


Window = Window((1200,600), "UI Box (Tile)")

UIBox = UIBox()
UIBox.size = 300,200
UIBox.center = Window.center
UIBox.open()

Dropdown = Dropdown(["one", "two", "three", ["one", "two"]])
Dropdown.center = UIBox.center
Dropdown.y = UIBox.y2 - Dropdown.h
UIBox.add(Dropdown)

Mouse = Mouse(Window)

while Window.is_open:

	if Window.is_focused:
		UIBox.controls(Key, Mouse, None)

		if Key.ENTER.pressed():
			UIBox.center = Window.center
			UIBox.open()
		if Key.BACKSPACE.pressed():
			UIBox.close()

	Window.clear((255,220,0))
	UIBox.draw(Window)
	Window.display(Mouse)