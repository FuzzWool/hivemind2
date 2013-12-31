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

	def _create_Bar(self, w,h):
		self.Bar = Box()
		self.Bar.size = w, 20
		self.children.append(self.Bar)

	# TOOL
	_Tools = []

	def _create_Tools(self):
		Nothing = self.Tool()
		#
		Tile = self.Tool()
		Tile.box_fill = Color(255,100,100)
		Tile.old_fill = Tile.box_fill
		Tile.hovered_color = Color(255,50,50)
		Tile.held_color = Color(255,0,0)
		#
		Camera = self.Tool()
		#
		self._Tools = [Nothing, Tile, Camera]

		#move
		Nothing.x += 500
		last_tool = None
		for tool in self._Tools:
			if last_tool: tool.x = last_tool.x2+1
			last_tool = tool

		#add
		for tool in self._Tools: self.children.append(tool)

	class Tool(Button):
		w,h = 50,50


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