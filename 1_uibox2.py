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

class Cell(_UI, Rectangle):
	x,y,w,h = 0,0,100,20
	name = "untitled_cell"

	def __init__(self, name):
		self.name = name

	def controls(self, Key, Mouse, Camera):
		self.hovered = self._hover(Mouse)
		self.selected = self._select(Mouse)

	def draw(self, Window):
		self.rect = self._create_rect()
		self.text = self._create_text()
		Window.draw(self.rect)
		Window.draw(self.text)


	############################

	hovered = False
	def _hover(self, Mouse):
		return Mouse.inside(self)

	selected = False
	def _select(self, Mouse):
		if Mouse.left.pressed():
			if self.hovered: return True
			else: return False
		return self.selected


	############################

	font = Font("speech")

	def _create_rect(self): #draw
		x,y = self.position
		w,h = self.size
		hovered = self.hovered
		selected = self.selected
		#
		rect = RectangleShape((w,h))
		rect.position = x,y
		rect.outline_color = Color.BLACK
		rect.outline_thickness = 1
		if hovered: rect.fill_color = Color(255,0,0)
		if selected: rect.fill_color = Color(200,200,200)
		#
		return rect

	def _create_text(self): #draw
		x,y = self.position
		x += 3; y += 3
		name = self.name
		#
		text = Text(self.font)
		text.write(name)
		text.position = x,y
		#
		return text




class Dropdown(Cell):

	name = "DROPDOWN"
	cells = []

	def __init__(self, cells):
		self.cells = self._create_cells(cells)

	def controls(self, Key, Mouse, Camera):
		if self.selected:
			for cell in self.cells:
				cell.controls(Key, Mouse, Camera)
		#
		Cell.controls(self, Key, Mouse, Camera)
		for cell in self.cells:
			if cell.selected:
				self.selected = True
				self.name = cell.name

	def draw(self, Window):
		self.cells = self._position_cells(self.cells)
		if self.selected:
			for cell in self.cells:
				cell.draw(Window)
		#
		Cell.draw(self, Window)


	###############################

	def _create_cells(self, cell_input): #init
		cells = []
		#
		for ci in cell_input:
			
			if type(ci) == str:
				cell = Cell(ci)
			if type(ci) == list:
				cell = Dropdown(ci)

			cells.append(cell)
		#
		return cells

	def _position_cells(self, cells): #draw
		x,y = self.position
		#
		for cell in cells:
			y += cell.h
			cell.position = x,y
		#
		return cells

#######################################


Window = Window((1200,600), "UI Box (Tile)")

UIBox = UIBox()
UIBox.size = 300,200
UIBox.center = Window.center
UIBox.open()

dropdown = Dropdown\
(["one", "two", "three", "four"])
# (["one", "two", "three", ["ONE", ["TWO", "THREE"]],["FOUR"]])
dropdown.center = UIBox.center
dropdown.y = UIBox.y2 - Dropdown.h
UIBox.add(dropdown)

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