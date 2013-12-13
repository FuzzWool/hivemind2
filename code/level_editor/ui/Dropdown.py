from code.level_editor.ui import UIBox, _UI
from sfml import RectangleShape
from sfml import Color
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
		if hovered: rect.fill_color = Color(225,225,225)
		if selected: rect.fill_color = Color(175,175,175)
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


class _Dropdown(object):
#A skeleton designed to be inherited by Dropdown cells.
#Provides cell event handling similarities.

	cells = []
	opened = False

	def __init__(self, input_cells):
		self.child = self._child()
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

	#######################################

	#DROPDOWN STATES
	class _child(object):
		
		#If another dropdown is open,
		#close the previous.
		_opened_dropdown = None
		@property
		def opened_dropdown(self):
			return self._opened_dropdown
		@opened_dropdown.setter
		def opened_dropdown(self, new_d):
			old_d = self.opened_dropdown
			if old_d != None:
				if old_d != new_d:
					old_d.opened = False
			self._opened_dropdown = new_d

	#######################################

	#CELL HANDLING
	def _init_cells(self, input_cells): #init
		cells = []
		r = self.root
		c = self.child
		#
		for input_cell in input_cells:
			if type(input_cell) == str:
				cell = Dropdown_Cell(input_cell,r)
			if type(input_cell) == list:
				cell = Dropdown_Dropdown(input_cell,r,c)
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

	#CONTROLS
	_opened = False
	@property
	def opened(self): return self._opened
	@opened.setter
	def opened(self, b):
		self._opened = b
		if b == False: self._close()
	#
	def _close(self):
		# Unselect all cells within it.
		# Close all dropdowns within it.
		for cell in self.cells:
			if type(cell) == Dropdown_Cell:
				cell.selected = False
				cell.hovered = False
			if type(cell) == Dropdown_Dropdown:
				cell.opened = False


class Dropdown(_Cell, _Dropdown):
# * Creates contained cells from a list.

	cells = []
	name = ""
	selected_name = ""
	hovered_name = ""

	def __init__(self, input_cells):
		_Cell.__init__(self, "-")
		_Dropdown.__init__(self, input_cells)
		self.root = self.root()

	def controls(self, Key, Mouse, Camera):
		self._open(Mouse)
		self.root.update()
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

		#Dropdown > Dropdown_Cell
		selected_cell = None
		hovered_cell = None

		selected_changed = False #for controls
		old_selected = None
		#
		def update(self):
			if self.selected_cell != self.old_selected:
				self.selected_changed = True
			else:
				self.selected_changed = False
			self.old_selected = self.selected_cell

	#######################################


	# opened = False

	#########
	#CONTROLS
	def _open(self, Mouse): #controls
		
		#Click the Dropdown.
		if Mouse.left.pressed():
			if Mouse.inside(self):
				self.opened = not self.opened

		#Click a selection.
		if self.root.selected_changed:
			if self.root.selected_cell != None:
				self.opened = False

	def _change_name(self):
		root = self.root
	
		if root.selected_cell != None:
			self.selected_name = root.selected_cell.name

		if root.hovered_cell != None:
			self.hovered_name = root.hovered_cell.name
		else:
			self.hovered_name = ""

		#

		name = self.name
		#
		if self.hovered_name != ""\
		and self.selected_name != "":
			name = "%s (%s)" \
			% (self.selected_name, self.hovered_name)
		elif self.hovered_name != "":
			name = "(%s)" % self.hovered_name
		elif self.selected_name != "":
			name = self.selected_name
		else:
			name = "..." 
		#
		self.name = name


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

	def __init__(self, input_cells, root, parent):
		if len(input_cells) < 1: raise "empty"
		self.root = root
		self.parent = parent
		_Cell.__init__(self, input_cells[0] + "...")
		_Dropdown.__init__(self, input_cells[1:])

	def update_graphics(self):
		_Cell.update_graphics(self)
		_Dropdown.update_graphics(self)

	def controls(self, Key, Mouse, Camera):
		self._open(Mouse)
		_Dropdown.controls(self, Mouse)

	def draw(self, Window):
		_Cell.draw(self, Window)
		_Dropdown.draw(self, Window)


	#######################################


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


	#PARENT STATES
	_opened = False
	@property
	def opened(self): return self._opened
	@opened.setter
	def opened(self, b):
		self._opened = b
		self.selected = b
		if b == True:
			self.parent.opened_dropdown = self
		if b == False:
			self._close()

	def _open(self, Mouse):
		if Mouse.inside(self):
			self.opened = True