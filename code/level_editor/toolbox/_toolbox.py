from tile import TileTool, CameraTool, EntityTool
#
from code.sfml_plus.ui import _UI, Box
from code.sfml_plus import TweenRectangle
from sfml import Color

#menus
from code.sfml_plus.ui import Dropdown


class ToolBox(_UI, TweenRectangle):
	
	#################################
	# PUBLIC

	def __init__(self, w,h):
		_UI.__init__(self)
		TweenRectangle.__init__(self)
		#
		self._create_Bar(w,h)
		self._create_Tools()
		self._init_Menus()
		self._init_states()
		#
		self.size = w,h

	def controls(self, Key, Mouse, Camera):
		_UI.controls(self, Key, Mouse, Camera)
		self._select_Tool(Key, Mouse, Camera)
		self._state_handling(Key, Mouse, Camera)

	def add_controls(self, WorldMap):
		self._add_controls(WorldMap)


	#

	def normal_draw(self, target, states):
		for child in self.children:
			try: child.normal_draw(target, states)
			except: pass

	def static_draw(self, target, states):
		_UI.draw(self, target, states)
		TweenRectangle.draw(self)
		for child in self.children:
			try: child.static_draw(target, states)
			except: pass

	#

	opened = True
	def toggle(self):
		self.opened = not self.opened
		if self.opened == True: self.tween.y = 0
		if self.opened == False: self.tween.y = -80



	#################################
	# PRIVATE

	_Tools = []
	_Menus = []

	###
	# STATES

	class states:
		hovered = False

	def _init_states(self):
		self.states = self.states()
		for tool in self._Tools:
			tool.parent_states = self.states

	def _state_handling(self, Key, Mouse, Camera):
		#hovered
		self.states.hovered = False
		for tool in self._Tools:
			if Mouse.inside(tool):
				self.states.hovered = True

	###
	# BAR

	Bar = None

	def _create_Bar(self, w,h): #init
		self.Bar = Box()
		self.Bar.size = w, 20
		self.children.append(self.Bar)


	###
	# TOOLS

	def _create_Tools(self): #init
		#create
		self._Tools = [TileTool(), CameraTool(), EntityTool()]
		self._selected_Tool = self._Tools[0]
		self._selected_Tool.active = True

		#move
		self._Tools[0].x += 400
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
					self._selected_Tool.open()
		#tool changed
		if self._old_Tool != None\
		and self._old_Tool != self._selected_Tool:
			self._old_Tool.close()

		self._old_Tool = self._selected_Tool

	def _add_controls(self, WorldMap):
		for tool in self._Tools:
			tool.add_controls(WorldMap)

	###
	# Menus

	def _init_Menus(self):
		File = Dropdown(["New","Save","Save As","Open"])
		File.text = "File"
		File.w = 50
		self.children.append(File)
		self._Menus.append(File)