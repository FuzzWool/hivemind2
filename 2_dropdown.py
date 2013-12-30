from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

##########################################

from code.sfml_plus.ui import Button, ToggleButton


class _Dropdown(ToggleButton):

	#################################
	# PUBLIC
	# * Makes cells by taking a list of cell names.

	text = "Untitled Dropdown"
	w = 125

	def __init__(self, cell_names):
		self.child = self.child()
		ToggleButton.__init__(self)
		self._create_cells(cell_names)
		self._position_cells()


	def controls(self, Key, Mouse, Camera):
		ToggleButton.controls(self, Key, Mouse, Camera)
		if self.held:
			self._control_cells(Mouse)
		self._close_dropdowns()

	def draw(self, target, states):
		self._move_cells()
		ToggleButton.draw(self, target, states)
		if self.held:
			self._draw_cells(target, states)


	#################################
	# PRIVATE
	# * Makes cell objects.
	
	# CELLS
	cells = []

	def _create_cells(self, cell_names): #init
		self.cells = []
		for name in cell_names:

			if type(name) == str:
				cell = Dropdown_Cell(name,self.root,self)
			if type(name) == list:
				cell = Dropdown_Dropdown(name,self.root,self)
			cell.w, cell.h = self.w, self.h
			self.cells.append(cell)

	def _position_cells(self):
		pass

	def _control_cells(self, Mouse): #controls
		for cell in self.cells:
			cell.controls(None, Mouse, None)

	def _move_cells(self): #draw
		#move
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		for cell in self.cells:
			cell.x += x_move
			cell.y += y_move

	def _draw_cells(self, target, states): #draw
		#alpha
		for cell in self.cells:
			cell.alpha = self.alpha
		#draw
		for cell in self.cells:
			target.draw(cell, states)


	# CHILD
	# Handle closing sub-dropdown menus upon conflict.

	class child: #init
		def __init__(self):
			self.held = None

	def _close_dropdowns(self): #controls
		for cell in self.cells:
			if cell.held and self.child.held != cell:
				cell.held = False
				cell.rise = cell.old_rise




class Dropdown(_Dropdown):
#A dropdown menu which may contain cells.
# LOGIC
	# * Toggle button. Opens and closes.
	# * Remembers the selected/hovered cells.
	# * The root parent to Sub_Dropdowns and Cells.


	#################################
	# PUBLIC
	# * Makes cells by taking a list of cell names.

	def __init__(self, cell_names):
		self.root = self.root()
		_Dropdown.__init__(self, cell_names)

	def controls(self, Key, Mouse, Camera):
		_Dropdown.controls(self, Key, Mouse, Camera)

		#root events
		if self.root.close_request == True:
			self.held = False
			self.rise = self.old_rise
			self.root.close_request = False
		self._rename()

	def draw(self, target, states):
		_Dropdown.draw(self, target, states)

	#################################
	# PRIVATE
	# * Makes cell objects.
	
	# CONTROLS
	def _rename(self):
		if self.root.selected_cell:
			name = self.root.selected_cell.text
			#path name
			scope = self.root.selected_cell
			path = ""
			while True:
				scope = scope.parent
				if scope == self: break
				path = scope.text+path
			#
			if path+name != self.text:
				self.text = path+name

	# ROOT
	# Passed down to every object.
	# Represent's the core selected/hovered item.
	
	parent = None

	class root:
		def __init__(self):
			self.hovered_cell = None
			self.selected_cell = None
			self.close_request = False

	# CELLS
	def _position_cells(self):
		total_h = self.h
		for cell in self.cells:
			cell.y = total_h
			total_h += cell.h




class Dropdown_Cell(Button):
# GRAPHICS
# * Named and positioned based on the parent Dropdown's contents.
# LOGIC
# * Forwards it's status to the root Dropdown.

	def __init__(self, name, root, parent):
		Button.__init__(self)
		self.text = name
		self.root = root
		self.parent = parent

	def controls(self, Key, Mouse, Camera):
		Button.controls(self, Key, Mouse, Camera)
		if self.selected:
			self.root.selected_cell = self
			self.root.close_request = True

		if self.hovered:
			self.root.hovered_cell = self
			self.parent.child.held = self


class Dropdown_Dropdown(_Dropdown):
# GRAPHICS
# * Names itself the first item in the list,
#   makes the others into cells.
# * Positions cells differently.
# LOGIC
# * Opens itself on hover,
# Parent closes any non-hovered ones on conflict.

	def __init__(self, cell_names, root, parent):
		if len(cell_names) == 0: raise "needs name and cells"
		self.text = cell_names[0]+"/"
		self.root = root
		self.parent = parent
		_Dropdown.__init__(self, cell_names[1:])

	def controls(self, Key, Mouse, Camera):
		_Dropdown.controls(self, Key, Mouse, Camera)

		#Parent controls
		if self.hovered:
			self.held = True
			self.rise = 0
			self.parent.child.held = self

		if not self.held:
			self.child.held = None
	#

	def _position_cells(self):
		y2 = self.y1
		for cell in self.cells:
			cell.y = y2
			cell.x = self.x2+1
			y2 = cell.y2

##########################################

from code.sfml_plus.ui import Box
from code.sfml_plus.ui import Accept_Button, Cancel_Button
from code.sfml_plus.ui import Horizontal_Slider, Vertical_Slider, SliderBox
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

#

l = [str(i) for i in range(2)]
l.append(["doggies"])
l[-1].append(["grown-ups","men","women"])
l[-1].append(["kids","boys","girls"])
l.append(["bunnies"])
l[-1].append(["grown-ups","men","women"])
l[-1].append(["kids","boys","girls"])
dropdown = Dropdown(l)
dropdown.y += 250
dropdown.x += (box1.w/2) - (dropdown.w/2)
box1.children.append(dropdown)

#

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