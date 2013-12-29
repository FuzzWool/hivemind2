from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

##########################################

from code.sfml_plus.ui import Button, ToggleButton

class Dropdown(ToggleButton):
#A dropdown menu which may contain cells.
# LOGIC
	# WIP - Toggle button. Opens and closes.
	# WIP - Remembers the paths/names of selected/hovered cells.
	# WIP - The root parent to Sub_Dropdowns and Cells.


	#################################
	# PUBLIC
	# * Makes cells by taking a list of cell names.

	text = "Dropdown"
	w = 125

	def __init__(self, cell_names):
		ToggleButton.__init__(self)
		self._create_cells(cell_names)

	def controls(self, Key, Mouse, Camera):
		ToggleButton.controls(self, Key, Mouse, Camera)
		if self.held:
			self._control_cells(Mouse)

	def draw(self, target, states):
		self._move_cells()
		ToggleButton.draw(self, target, states)
		if self.held:
			self._draw_cells(target, states)

	#################################
	# PRIVATE
	# * Makes cell objects.
	
	cells = []

	def _create_cells(self, cell_names): #init
		self.cells = []
		total_h = self.h + self.old_rise
		for name in cell_names:
			cell = Dropdown_Cell(name)
			cell.size = self.size
			cell.y = total_h
			self.cells.append(cell)
			total_h += cell.h

	def _control_cells(self, Mouse): #controls
		for cell in self.cells:
			pass

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




class Dropdown_Cell(Button):

	def __init__(self, name):
		Button.__init__(self)
		self.text = name

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

l = ["one", "two", "three"]
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