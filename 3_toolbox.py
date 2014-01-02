from code.sfml_plus import Window
from code.sfml_plus import Key, Mouse, Camera

##########################################

from code.sfml_plus.ui import _UI, Box, Button
from code.sfml_plus import TweenRectangle
from sfml import Color

#Tile
from code.sfml_plus.ui import Box, Dropdown
from code.level_editor.ui import TileSelector

class ToolBox(_UI, TweenRectangle):
	
	#################################
	# PUBLIC

	def __init__(self, w,h):
		_UI.__init__(self)
		TweenRectangle.__init__(self)
		self._create_Bar(w,h)
		self._create_Tools()
		self.size = w,h

	def controls(self, Key, Mouse, Camera):
		_UI.controls(self, Key, Mouse, Camera)
		self._select_Tool(Key, Mouse, Camera)
		self._control_Tool(Key, Mouse, Camera)

	def draw(self, target, states):
		TweenRectangle.draw(self)
		_UI.draw(self, target, states)

	#

	opened = True
	def toggle(self):
		self.opened = not self.opened
		if self.opened == True: self.tween.y = 0
		if self.opened == False: self.tween.y = -80


	#################################
	# PRIVATE


	# BAR
	Bar = None

	def _create_Bar(self, w,h): #init
		self.Bar = Box()
		self.Bar.size = w, 20
		self.children.append(self.Bar)


	# TOOLS
	_Tools = []
	
	def _create_Tools(self): #init
		#create
		self._Tools = [_Tool(), Tile()]

		#move
		last_tool = None
		for tool in self._Tools:
			if last_tool: tool.x = last_tool.x2+1
			last_tool = tool

		#add
		for tool in self._Tools: self.children.append(tool)


	_old_Tool = None
	_selected_Tool = None
	def _select_Tool(self, Key, Mouse, Camera): #controls
		#tool selected
		if Mouse.left.pressed():
			for tool in self._Tools:
				if Mouse.inside(tool):
					self._selected_Tool = tool
		#tool changed
		if self._old_Tool != None\
		and self._old_Tool != self._selected_Tool:
			self._old_Tool.close()

		self._old_Tool = self._selected_Tool




	def _control_Tool(self, Key, Mouse, Camera): #controls
		if self._selected_Tool != None:
			self._selected_Tool.active_controls(Key, Mouse, Camera)


#

class _Tool(Button):
# GRAPHICS
	# * A tile-shape.
# LOGIC
	# * 'Selected' state controlled externally.
	#	 Has special 'active' controls for it.

	w,h = 80,80

	def __init__(self):
		Button.__init__(self)
		self.text = ""

	#

	def active_controls(self, Key, Mouse, Camera):
	#Controls the tool uses only while active.
		pass

	def close(self):
	#Close all Windows the Tool has opened.
		pass



class Tile(_Tool):

	#################################
	# PUBLIC

	box_fill = Color(255,100,100)
	old_fill = box_fill
	hovered_color = Color(255,50,50)
	held_color = Color(255,0,0)

	def __init__(self):
		_Tool.__init__(self)
		self.Selector = self.Selector()
		self.Selector.position = 300,150
		self.Selector.y += 20

	def active_controls(self, Key, Mouse, Camera):
		if Key.SPACE.held():
			self.Selector.open()
			self.Selector.controls(Key, Mouse, Camera)
		else:
			self.Selector.close()

	def close(self):
		self.Selector.close()

	def draw(self, target, states):
		_Tool.draw(self, target, states)
		target.draw(self.Selector)


	#################################
	# PRIVATE

	class Selector(Box):
		#A window for editing tiles.
		
		def __init__(self):
			Box.__init__(self)
			self.size = 550,275
			self._add_widgets()

		#
		
		def _add_widgets(self):
			#
			tileselector = TileSelector()
			tileselector.tile_x += 1
			tileselector.tile_y += 1
			self.children.append(tileselector)
			#
			l = ["filler1","filler2"]
			dropdown = Dropdown(l)
			dropdown.center = self.center
			dropdown.y = self.y2 - dropdown.h
			self.children.append(dropdown)




##########################################

Window = Window((1200,600), "ToolBox")
ToolBox = ToolBox(*Window.size)

Camera = Camera(Window)
Mouse = Mouse(Window)

while Window.is_open:
	if Window.is_focused:
		ToolBox.controls(Key, Mouse, Camera)
		
		if Key.TAB.pressed(): ToolBox.toggle()

	Window.clear((255,220,0))
	Window.draw(ToolBox)
	Window.display(Mouse)