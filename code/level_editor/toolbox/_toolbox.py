from tile import TileTool, CameraTool, EntityTool
#
from code.sfml_plus.ui import _UI, Box, Button
from code.sfml_plus import TweenRectangle
from sfml import Color

#menus
from code.sfml_plus.ui import Dropdown
from code.sfml_plus.ui import InputBox
from code.sfml_plus.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class ToolBox(_UI, TweenRectangle):
	
	#################################
	# PUBLIC

	def __init__(self, w,h):
		_UI.__init__(self)
		TweenRectangle.__init__(self)
		self._create_Bar(w,h)
		self._create_Tools()
		self._create_Menus()
		self._init_states()
		self.size = SCREEN_WIDTH, SCREEN_HEIGHT

	#

	def controls(self, Key, Mouse, Camera):
		_UI.controls(self, Key, Mouse, Camera)
		self._state_handling(Key, Mouse, Camera)

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
			self._Menus.close()


	#################################
	# PRIVATE

	Bar = None
	_Tools = None
	_Menus = None

	###
	# States (shared with the tools)
	# in_use - The ToolBox is being interacted with.

	class states:
		in_use = False

	def _init_states(self):
		self.states = self.states()
		for tool in self._Tools.children:
			tool.parent_states = self.states

	def _state_handling(self, Key, Mouse, Camera):
		#Check to see if any widgets are in use.
		self.states.in_use = False
		for widget in [self.Bar]+self._Tools.children+self._Menus.children:
			_p = [widget.x1, widget.y1, widget.x2, widget.y2+widget.rise]
			if Mouse.inside(_p):
				self.states.in_use = True
			try:
				if widget.held:
					self.states.in_use = True
			except:
				pass
			try:
				if widget.in_use:
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

	def _create_Tools(self):
		self._Tools = self._Tools()
		self.children.append(self._Tools)

	def _add_controls(self, WorldMap):
		self._Tools.add_controls(WorldMap)

	class _Tools(_UI):

		#################################
		# PUBLIC

		children = []

		def __init__(self):
			_UI.__init__(self)
			self._create_Tools()
			self.size = SCREEN_WIDTH-1, SCREEN_HEIGHT-1

		def controls(self, Key, Mouse, Camera):
			_UI.controls(self, Key, Mouse, Camera)
			self._select_Tool(Key, Mouse, Camera)

		def add_controls(self, WorldMap):
			self._add_controls(WorldMap)

		def normal_draw(self, target, states):
			# _UI.draw(self, target, states)
			for child in self.children:
				child.normal_draw(target, states)

		def static_draw(self, target, states):
			for child in self.children:
				child.static_draw(target, states)

		#################################
		# PUBLIC

		def _create_Tools(self): #init
			#create
			self._Tools = [TileTool(), CameraTool(), EntityTool()]
			self._selected_Tool = self._Tools[0]
			self._selected_Tool.active = True

			#release cap
			for tool in self._Tools:
				tool.size_cap = False

			#move
			self._Tools[0].x += 300
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

	def _create_Menus(self):
		self._Menus = self._Menus()
		self.children.append(self._Menus)

	class _Menus(_UI):
	# * Contains the Windows to respond to Menu event handling. 

		#################################
		# PUBLIC

		children = []

		def __init__(self):
			_UI.__init__(self)
			self.size = SCREEN_WIDTH-1, SCREEN_HEIGHT-1
			self._create_Menus()

		def controls(self, Key, Mouse, Camera):
			_UI.controls(self, Key, Mouse, Camera)

		#

		def close(self):
			for child in self.children:
				child.held = False
				child.rise = child.old_rise

		#################################
		# PRIVATE

		def _create_Menus(self):
			self.children.append(self._File())

		class _File(Dropdown):
		# File-specific Windows.

			#################################
			# PUBLIC

			in_use = False

			def __init__(self):
				Dropdown.__init__(self, ["New","Save","Save As","Open"])
				self.size_cap = False
				self.text = "File"
				self.w = 50

			def controls(self, Key, Mouse, Camera):
				Dropdown.controls(self, Key, Mouse, Camera)
				self._remove_empty()
				self._text_action()

			def draw(self, target, states):
				Dropdown.draw(self, target, states)

			#################################
			# PRIVATE

			###
			# Boxes

			old_action = "File"
			def _text_action(self):
				action = self.text
				if action != self.old_action:
					self._act(action)
				self.old_action = action
				self.text = "File"

			def _act(self, action): #
				#Close old children.
				for child in self.children:
					child.close()
				#Open new ones.
				if action == "Save As":
					box = self._SaveAs()
					box.follow = False
					box.open()
					self.children.append(box)

			#

			def _remove_empty(self):
				#Remove any completely transparent boxes.
				def removal(arg):
					for l in arg:
						if l.alpha != 0: yield l
				self.children = list(removal(self.children))

			###

			class _New(Box):
				pass

			###

			class _Save(Box):
				pass

			###

			class _SaveAs(Box):
				def __init__(self):
					Box.__init__(self)
					self.children.append(InputBox())
					self.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2

			###

			class _Open(Box):
				pass