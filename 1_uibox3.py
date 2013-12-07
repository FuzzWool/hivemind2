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
# A consistent base for Dropdowns, Cells and SubDropdowns.
# Represents only a GRAPHICAL cell.

	name = "untitled"
	x,y,w,h = 0,0,100,20

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
		#
		rect = RectangleShape((w,h))
		rect.position = x,y
		rect.outline_color = Color.BLACK
		rect.outline_thickness = 1
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



class Dropdown(_Cell):
# A cell containing a list of other cells.
# The root cell represents the selected cell.  

	cells = []
	x,y,w,h = 0,0,100,20

	def __init__(self, input_cells):
		_Cell.__init__(self, "-")
		self.cells = self._create_cells(input_cells)

	def update_graphics(self):
		_Cell.update_graphics(self)
		self.cells = self._position_cells(self.cells)
		for cell in self.cells:
			cell.update_graphics()
			for graphic in cell.graphics:
				self.graphics.append(graphic)

	def draw(self, Window):
		_Cell.draw(self, Window)
		for cell in self.cells:
			cell.draw(Window)

	#######################################

	#init
	def _create_cells(self, input_cells):
		cells = []
		for ci in input_cells:
			cell = Dropdown_Cell(ci)
			cells.append(cell)
		return cells


	#update_graphics
	def _position_cells(self, cells):
		x,y = self.position
		#
		for cell in cells:
			y += cell.h
			cell.position = x,y
		#
		return cells


	#draw
	pass


class Dropdown_Cell(_Cell):
# WIP - For handling Dropdown-specific communication.

	def __init__(self, name):
		_Cell.__init__(self, name)

	def update_graphics(self):
		_Cell.update_graphics(self)

	def draw(self, Window):
		_Cell.draw(self, Window)

	#######################################

	pass


class Dropdown_Dropdown(_UI):
# A dropdown menu contained within a dropdown menu.
	pass


#######################################


Window = Window((1200,600), "UI Box (Tile)")

UIBox1 = UIBox()
UIBox1.size = 300,200
UIBox1.center = Window.center
UIBox1.open()

dropdown = Dropdown\
(["one", "two", "three", "four"])
# (["one", "two", "three", ["ONE", ["TWO", "THREE"]]])
# (["one", "two", "three", ["four"])
dropdown.center = UIBox1.center
dropdown.y = UIBox1.y2 - Dropdown.h
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