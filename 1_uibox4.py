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
			UI.update_graphics()

		if self.active:
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

	active = True

	def open(self):
		self.active = True

		amt = 20
		self.y += amt
		self.Smooth.y = self.y - amt
		self._alpha = 0
		self._end_alpha = 255

	def close(self):
		self.active = False

		amt = 20
		self.Smooth.y = self.y + amt
		self._alpha = 255
		self._end_alpha = 0


######

class _UI(Rectangle):

	x,y,w,h = 0,0,0,0
	graphics = []

	def controls(self, Key, Mouse, Camera):
		pass

	def update_graphics(self):
		pass

	def draw(self, Window):
		pass


from code.sfml_plus.graphics import Font, Text
class _Cell(_UI):
# A basic cell graphic: A box and text.
# Basic graphical states, too.

	name = "untitled"
	x,y,w,h = 0,0,100,20
	hovered = False
	selected = False

	def __init__(self, name):
		self.name = name

	def update_graphics(self):
		self.rect = self._create_rect()
		self.text = self._create_text()
		self.graphics = [self.rect, self.text]

	def draw(self, Window):
		Window.draw(self.rect)
		Window.draw(self.text)

	#######################################

	#update_graphics
	font = Font("speech")

	def _create_rect(self):
		x,y = self.position
		w,h = self.size
		hovered = self.hovered
		selected = self.selected
		#
		rect = RectangleShape((w,h))
		rect.position = x,y
		rect.outline_color = Color.BLACK
		rect.outline_thickness = 1
		if hovered: rect.fill_color = Color(200,200,200)
		if selected: rect.fill_color = Color(100,100,100)
		#
		return rect

	def _create_text(self): #update_graphics
		x,y = self.position
		x += 3; y += 3
		name = self.name
		#
		text = Text(self.font)
		text.write(name)
		text.position = x,y
		#
		return text


class _Dropdown:
#A skeleton designed to be inherited by Dropdown cells.
#Provides cell event handling similarities.

	cells = []
	opened = False

	def __init__(self, input_cells):
		self.cells = self._init_cells(input_cells)

	def update_graphics(self):
		self.cells = self._position_cells(self.cells)
		for cell in self.cells:
			cell.update_graphics()
			for graphic in cell.graphics:
				self.graphics.append(graphic)

	def controls(self, Mouse):
		self._cells_controls(Mouse)

	def draw(self, Window):
		self._draw_cells(Window)

	#

	def _init_cells(self, input_cells): #init
		cells = []
		root = self.root
		#
		for input_cell in input_cells:
			if type(input_cell) == str:
				cell = Dropdown_Cell(input_cell, root)
			if type(input_cell) == list:
				cell = Dropdown_Dropdown(input_cell, root)
			cells.append(cell)
		#
		return cells

	def _position_cells(self, cells): #update_graphics
		x,y = self.position
		#
		for cell in cells:
			y += Dropdown_Cell.h
			cell.position = x,y
		#
		return cells

	def _cells_controls(self, Mouse): #controls
		if self.opened:
			for cell in self.cells:
				cell.controls(None, Mouse, None)

	def _draw_cells(self, Window): #draw
		if self.opened:
			for cell in self.cells:
				cell.draw(Window)


class Dropdown(_Cell, _Dropdown):
# * Creates contained cells from a list.

	cells = []

	def __init__(self, input_cells):
		_Cell.__init__(self, "-")
		_Dropdown.__init__(self, input_cells)

	def controls(self, Key, Mouse, Camera):
		self._open_close(Mouse)
		_Dropdown.controls(self, Mouse)

	def update_graphics(self):
		_Cell.update_graphics(self)
		_Dropdown.update_graphics(self)
		self._change_name()

	def draw(self, Window):
		_Cell.draw(self, Window)
		_Dropdown.draw(self, Window)

	#######################################

	class root:
	#Cells communicating directly with the root.
	#(So event handling may be independant)
		selected_cell = None
		hovered_cell = None

	#######################################


	opened = False

	#########
	#CONTROLS
	def _open_close(self, Mouse): #controls
		if Mouse.left.pressed():
			if Mouse.inside(self):
				self.opened = True

	def _change_name(self):
		if self.root.selected_cell != None:
			self.name = self.root.selected_cell.name
		else:
			self.name = "-"



class Dropdown_Cell(_Cell):
# Event handling is the responsibility of the parent.
# Some states are forwarded to the root parent.

	def __init__(self, name, root):
		self.name = name
		self.root = root

	def controls(self, Key, Mouse, Camera):
		self._hover(Mouse)
		self._select(Mouse)

	#######################################

	#ROOT STATES
	root = None	
	_hovered = False
	_selected = False

	@property
	def hovered(self): return self._hovered
	@hovered.setter
	def hovered(self, b):
		self._hovered = b
		if b == True:
			self.root.hovered_cell = self
		if b == False:
			if self.root.hovered_cell == self:
				self.root.hovered_cell = None

	@property
	def selected(self): return self._selected
	@selected.setter
	def selected(self, b):
		self._selected = b
		if b == True:
			self.root.selected_cell = self
		if b == False:
			if self.root.selected_cell == self:
				self.root.selected_cell = None

	#

	def _hover(self, Mouse):
		self.hovered = Mouse.inside(self)

	def _select(self, Mouse):
		if Mouse.left.pressed():
			self.selected = self.hovered



class Dropdown_Dropdown(_Cell, _Dropdown):

	def __init__(self, input_cells, root):
		if len(input_cells) < 1: raise "empty"
		self.root = root
		_Cell.__init__(self, input_cells[0])
		_Dropdown.__init__(self, input_cells[1:])

	def update_graphics(self):
		_Cell.update_graphics(self)
		_Dropdown.update_graphics(self)

	def controls(self, Key, Mouse, Camera):
		_Dropdown.controls(self, Mouse)

	def draw(self, Window):
		_Cell.draw(self, Window)
		_Dropdown.draw(self, Window)


	#######################################

	opened = True

	def _position_cells(self, cells): #update_graphics
		x,y = self.position
		x += Dropdown_Cell.w+1
		y -= Dropdown_Cell.h
		#
		for cell in cells:
			y += Dropdown_Cell.h
			cell.position = x,y
		#
		return cells

#######################################


Window = Window((1200,600), "UI Box (Tile)")

UIBox1 = UIBox()
UIBox1.size = 300,200
UIBox1.center = Window.center
UIBox1.open()

dropdown = Dropdown\
(["a","b","c", ["A", "aa", "bb"]])
# (["a","b","c"])
dropdown.center = UIBox1.center
dropdown.y = UIBox1.y2 - dropdown.h
UIBox1.add(dropdown)

Mouse = Mouse(Window)

while Window.is_open:

	if Window.is_focused:
		UIBox1.controls(Key, Mouse, None)

		if Key.ENTER.pressed():
			UIBox1.center = Window.center
			UIBox1.open()
		if Key.BACKSPACE.pressed():
			UIBox1.close()

	Window.clear((255,220,0))
	UIBox1.draw(Window)
	Window.display(Mouse)