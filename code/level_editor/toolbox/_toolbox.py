from tile import TileTool, CameraTool, EntityTool
#
from code.sfml_plus.ui import _UI, Box, Button
from code.sfml_plus import TweenRectangle
from sfml import Color

#menus
from code.sfml_plus.ui import Dropdown
from code.sfml_plus.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class ToolBox(_UI, TweenRectangle):
	
	#################################
	# PUBLIC

	def __init__(self, w,h):
		_UI.__init__(self)
		TweenRectangle.__init__(self)
		#
		self._create_Bar(w,h)
		self._create_Tools()
		self._init_states()
		#
		self.Menus = self._Menus()
		#
		self.size = w,h

	def controls(self, Key, Mouse, Camera):
		_UI.controls(self, Key, Mouse, Camera)
		self._select_Tool(Key, Mouse, Camera)
		self.Menus.controls(Key, Mouse, Camera)

	def add_controls(self, WorldMap):
		self._add_controls(WorldMap)


	#

	def normal_draw(self, target, states):
		for child in self.children:
			try: child.normal_draw(target, states)
			except: pass

	def static_draw(self, target, states):
		TweenRectangle.draw(self)
		_UI.draw(self, target, states)
		self.Menus.draw(target, states)
		for child in self.children:
			try: child.static_draw(target, states)
			except: pass

	#

	opened = True
	def toggle(self):
		self.opened = not self.opened
		if self.opened == True: self.tween.y = 0
		if self.opened == False:
			self.tween.y = -80
			# self._hide_Menus()



	#################################
	# PRIVATE

	Bar = None
	_Tools = []
	_Menus = []

	###
	# States (shared with the tools)
	# in_use - The ToolBox is being interacted with.

	class states:
		in_use = False

	def _init_states(self):
		self.states = self.states()
		for tool in self._Tools:
			tool.parent_states = self.states

	def _state_handling(self, Key, Mouse, Camera):
		#Check to see if any widgets are in use.
		self.states.in_use = False
		for widget in [self.Bar] + self._Tools + self.Menus.children:
			_p = [widget.x1, widget.y1, widget.x2, widget.y2+widget.rise]
			if Mouse.inside(_p):
				self.states.in_use = True
			
			try:
				if widget.held:
					self.states.in_use = True
			except:
				pass


	###
	# Bar

	def _create_Bar(self, w,h): #init
		self.Bar = Box()
		self.Bar.size = w, 20
		self.children.append(self.Bar)


	###
	# Tools

	def _create_Tools(self): #init
		#create
		self._Tools = [TileTool(), CameraTool(), EntityTool()]
		self._selected_Tool = self._Tools[0]
		self._selected_Tool.active = True

		#move
		self._Tools[0].x += 400
		last_tool = None
		for tool in self._Tools:
			if last_tool: tool.x = last_tool.x2-1
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

	#_Menus

	# old_action = "File"
	# def _control_Menus(self): #controls
	# 	#File actions (based on text)
	# 	action = self.File.text
	# 	if action != self.old_action:
	# 		print action
	# 		# if action == "New":
	# 		# 	print 0
	# 		# if action == "Save":
	# 		# 	print 1
	# 		# if action == "Save As":
	# 		# 	print 2
	# 		# if action == "Open":
	# 		# 	print 3
	# 	self.old_action = action
	# 	self.File.text = "File"

	# #

	# def _hide_Menus(self): #toggle close
	# 	for menu in self._Menus:
	# 		menu.held = False
	# 		menu.rise = menu.old_rise


	class _Menus(_UI):
	# * Contains the Windows to respond to Menu event handling. 

		#################################
		# PUBLIC

		children = []

		def __init__(self):
			_UI.__init__(self)
			self._init_File()

		def controls(self, Key, Mouse, Camera):
			_UI.controls(self, Key, Mouse, Camera)

		def draw(self, target, states):
			_UI.draw(self, target, states)


		#################################
		# PRIVATE

		###
		# File

		_File = None

		def _init_File(self):
			File = self._File()
			self._File = self._File()
			self.children.append(File)
			self.size = SCREEN_WIDTH, SCREEN_HEIGHT

		class _File(Dropdown):
		# File-specific Windows.

			#################################
			# PUBLIC

			def __init__(self):
				Dropdown.__init__(self, ["New","Save","Save As","Open"])
				self.text = "File"
				self.w = 50

			def controls(self, Key, Mouse, Camera):
				Dropdown.controls(self, Key, Mouse, Camera)

			#################################
			# PRIVATE

			old_text = "File"
			def _text_action(self):
				pass

			class _New:
				pass

			class _Save:
				pass

			class _SaveAs:
				pass

			class _Open:
				pass