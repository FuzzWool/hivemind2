from code.sfml_plus import Window
from code.sfml_plus import Key, Mouse, Camera

##########################################

from code.sfml_plus.ui import _UI, Box, Button
from code.sfml_plus import TweenRectangle
from sfml import Color

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


	# CONTROLS


	# BAR
	Bar = None

	def _create_Bar(self, w,h):
		self.Bar = Box()
		self.Bar.size = w, 20
		self.children.append(self.Bar)


	# TOOLS
	_Tools = []
	
	def _create_Tools(self):
		#create
		self._Tools = [_Tool(), Tile()]

		#move
		last_tool = None
		for tool in self._Tools:
			if last_tool: tool.x = last_tool.x2+1
			last_tool = tool

		#add
		for tool in self._Tools: self.children.append(tool)


	_selected_Tool = None
	def _select_Tool(self, Key, Mouse, Camera):
		if Mouse.left.pressed():
			for tool in self._Tools:
				if Mouse.inside(tool):
					self._selected_Tool = tool

	def _control_Tool(self, Key, Mouse, Camera):
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

	def active_controls(self, Key, Mouse, Camera):
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

	def active_controls(self, Key, Mouse, Camera):
		print "Tile Tool active"


	#################################
	# PRIVATE

	pass




##########################################

Window = Window((1200,600), "ToolBox")
ToolBox = ToolBox(*Window.size)

Camera = Camera(Window)
Mouse = Mouse(Window)

while Window.is_open:
	if Window.is_focused:
		ToolBox.controls(Key, Mouse, Camera)
		
		if Key.ENTER.pressed(): ToolBox.toggle()

	Window.clear((255,220,0))
	Window.draw(ToolBox)
	Window.display(Mouse)