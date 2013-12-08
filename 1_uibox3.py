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
# * Core event handling for Dropdown menus.
#   Provides for any cells under it's wing.
# * It's own _Cell functions need manual settings.

	cells = []
	graphics = []

	def __init__(self, input_cells):
		self.cells = self._create_cells(input_cells)

	def update_graphics(self):
		self.cells = self._position_cells(self.cells)
		for cell in self.cells:
			cell.update_graphics()
			for graphic in cell.graphics:
				self.graphics.append(graphic)

	def controls(self, Key, Mouse, Camera):
		self._open(Mouse)
		self._cell_controls(Mouse)

	def draw(self, Window):
		self._draw_cells(Window)


	######################################

	opened = False

	#UPDATE_GRAPHICS
	def _position_cells(self, cells):
		raise "Set _position_cells!"

	#CONTROLS
	def _open(self, Mouse):
		raise "Set _open!"

	#

	#INIT
	def _create_cells(self, input_cells):
		cells = []
		for ci in input_cells:
			if type(ci) == str:
				cell = Dropdown_Cell(ci)
			if type(ci) == list:
				cell = Dropdown_Dropdown(ci)
			cells.append(cell)
		return cells


	#CONTROLS
	def _cell_controls(self, Mouse):
	#Shared event handling for Cells and Dropdowns.
		if not self.opened: return
		for cell in self.cells:
			cell.controls(Mouse)

	#DRAW
	def _draw_cells(self, Window):
		if not self.opened: return
		for cell in self.cells:
			cell.draw(Window)



class Dropdown(_Cell, _Dropdown):
# * A cell containing other cells.
#   It tucks them away inside a toggleable list.
# * This is the root Dropdown menu.
#   It positions cells differently, and changes it's name.

	x,y,w,h = 0,0,100,20

	def __init__(self, input_cells):
		_Cell.__init__(self, "-")
		_Dropdown.__init__(self, input_cells)

	def update_graphics(self):
		_Cell.update_graphics(self)
		_Dropdown.update_graphics(self)

	def controls(self, Key, Mouse, Camera):
		_Cell.controls(self, Key, Mouse, Camera)
		_Dropdown.controls(self, Key, Mouse, Camera)
		self._change_name()

	def draw(self, Window):
		_Cell.draw(self, Window)
		_Dropdown.draw(self, Window)

	#######################################

	cells = []
	opened = False

	#UPDATE_GRAPHICS
	def _position_cells(self, cells):
		x,y = self.position
		#
		for cell in cells:
			y += cell.h
			cell.position = x,y
		#
		return cells

	#CONTROLS
	def _open(self, Mouse):
		opened = self.opened
		inside_cells = False
		for cell in self.cells:
			if Mouse.inside(cell):
				inside_cells = True
		#
		if Mouse.left.pressed():
			if Mouse.inside(self):
				opened = not self.opened
			elif not inside_cells:
				opened = False
		#
		self.opened = opened

	def _change_name(self):
		if not self.opened: return
		for cell in self.cells:
			if cell.selected:
				self.name = cell.name


class Dropdown_Cell(_Cell):
# Simple event handling.

	hovered = False
	selected = False

	def controls(self, Mouse):
		self.hovered = Mouse.inside(self)

		if Mouse.left.pressed():
			if self.hovered: self.selected = True
			else: self.selected = False



class Dropdown_Dropdown(_Cell, _Dropdown):
# A dropdown menu contained within a dropdown menu.

	def __init__(self, cells):
		if len(cells) <= 1: raise "empty"
		_Cell.__init__(self, cells[0])
		_Dropdown.__init__(self, cells[1:])

	def update_graphics(self):
		_Cell.update_graphics(self)
		_Dropdown.update_graphics(self)

	def controls(self, Mouse):
		_Dropdown.controls(self, None, Mouse, None)

	def draw(self, Window):
		_Cell.draw(self, Window)
		_Dropdown.draw(self, Window)


	#######################################

	opened = True

	#UPDATE_GRAPHICS
	def _position_cells(self, cells):
		x,y = self.position
		x += _Cell.w+1
		y -= _Cell.h
		#
		for cell in cells:
			y += _Cell.h
			cell.position = x,y
		#
		return cells

	#CONTROLS
	def _open(self, Mouse):
		if Mouse.inside(self):
			self.hovered = True
		else:
			self.hovered = False
		self.opened = self.hovered


#######################################


Window = Window((1200,600), "UI Box (Tile)")

UIBox1 = UIBox()
UIBox1.size = 300,200
UIBox1.center = Window.center
UIBox1.open()

dropdown = Dropdown\
(["one", "two", "three", ["ONE", "TWO", "THREE"]])
# (["one", "two", "three", "four"])
# (["one", "two", "three", ["four"])
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