from code.sfml_plus.ui import _UI, Box, Button
from code.sfml_plus import TweenRectangle
from sfml import Color

#Tool
from code.sfml_plus import Texture, MySprite

#Tile
from code.sfml_plus.ui import Box, Dropdown
from code.level_editor.ui import TileSelector, Cursor

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

	def add_controls(self, WorldMap):
		self._add_controls(WorldMap)


	def draw(self, target, states):
		_UI.draw(self, target, states)
		TweenRectangle.draw(self)

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


#

class _Tool(Button):
# GRAPHICS
	# * A tile-shape.
# LOGIC
	# * 'Selected' state controlled externally.
	#	 Has special 'active' controls for it.


	#################################
	# PUBLIC

	w,h = 80,50
	active = False
	texture_clip = 0

	class deactive_colors:
		normal_color = Color(240,240,240)
		hovered_color = Color(255,255,255)
		held_color = hovered_color
		selected_color = hovered_color

	class active_colors:
		normal_color = Color(240,240,240)
		hovered_color = Color(255,255,255)
		held_color = hovered_color
		selected_color = hovered_color

	#

	def __init__(self):
		Button.__init__(self)
		self.text = ""
		self.active = False
		self._init_sprite()

	def controls(self, Key, Mouse, Camera):
		Button.controls(self, Key, Mouse, Camera)
	
	def add_controls(self, WorldMap):
		pass

	def draw(self, target, states):
		self._apply_coloring()
		Button.draw(self, target, states)
		self._draw_sprite(target, states)

	#

	def open(self):
	#Create all Windows for the Tool.
		self.active = True

	def close(self):
	#Close all windows for the Tool.
		self.active = False


	#################################
	# PRIVATE

	# Color
	def _init_coloring(self):
		self.active_colors = self.active_colors()
		self.deactive_colors = self.deactive_colors()

	def _apply_coloring(self):
		if self.active: group = self.active_colors
		if not self.active: group = self.deactive_colors
		#
		self.box_fill = group.normal_color
		if self.hovered:
			self.box_fill = group.hovered_color
		if self.held:
			self.box_fill = group.held_color
		if self.selected:
			self.box_fill = group.selected_color

	#Sprite
	def _init_sprite(self):
		texture = Texture.from_file("assets/ui/tools.png")
		self.sprite = MySprite(texture)
		self.sprite.clip.set(80,50)
		self.sprite.clip.use(self.texture_clip, 0)

	def _draw_sprite(self, target, states):
		self.sprite.center = self.center
		self.sprite.y -= self.rise_offset
		target.draw(self.sprite, states)



class TileTool(_Tool):

	#################################
	# PUBLIC

	active = False
	texture_clip = 0

	class active_colors:
		normal_color = Color(255,0,0)
		hovered_color = Color(255,100,100)
		held_color = hovered_color
		selected_color = hovered_color

	#

	def __init__(self):
		_Tool.__init__(self)
		#Selector
		self.Selector = self._Selector()
		self.Selector.position = 300,150
		self.Selector.y += 20
		#Cursor
		self.Cursor = Cursor()
		self.Cursor.expand = False

	def draw(self, target, states):
		#Cursor
		if not self.Selector.opened and self.active:
			self.Cursor.draw(target, states)
		#Selector
		target.draw(self.Selector, states)
		_Tool.draw(self, target, states)

	#

	def controls(self, Key, Mouse, Camera):
		_Tool.controls(self, Key, Mouse, Camera)
		if self.active:

			#Selector
			if Key.SPACE.held():
				self.Selector.open()
				self.Selector.controls(Key, Mouse, Camera)
			else:
				self.Selector.close()

			#Cursor
			if not self.Selector.opened:
				self.Cursor.controls(Key, Mouse, Camera)

	def add_controls(self, WorldMap):
		if not self.active: return
		
		pass

	def open(self):
		_Tool.open(self)

	def close(self):
		_Tool.close(self)
		self.Selector.close()

	#################################
	# PRIVATE


	class _Selector(Box):
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


class CameraTool(_Tool):

	#################################
	# PUBLIC

	active = False
	texture_clip = 1

	class active_colors:
		normal_color = Color(100,100,100)
		hovered_color = Color(150,150,150)
		held_color = hovered_color
		selected_color = hovered_color


class EntityTool(_Tool):

	#################################
	# PUBLIC

	active = False
	texture_clip = 2

	class active_colors:
		normal_color = Color(0,255,0)
		hovered_color = Color(100,255,100)
		held_color = hovered_color
		selected_color = hovered_color