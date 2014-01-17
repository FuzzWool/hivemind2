from _tool import _Tool
#
import os
from code.sfml_plus.constants import ROOM_WIDTH, ROOM_HEIGHT
from code.sfml_plus.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from code.game.worldmap import TILESHEET_CAP
from sfml import Color
from code.sfml_plus.ui import Box, Dropdown
from code.level_editor.ui import TileSelector, Cursor


class TileTool(_Tool):

	#################################
	# PUBLIC

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
		self.Selector.center = (SCREEN_WIDTH/2),0
		self.Selector.y = 150
		self.Selector.y += 20
		#Cursor
		self.Cursor = Cursor()
		self.Cursor.expand = False
		self.Cursor.absolute = True
		#Help
		c = str(TILESHEET_CAP)
		t = "---------------------------\n"
		t=t+"TILE TOOL\n"
		t=t+"---------------------------\n"
		t=t+"\n"
		t=t+"GENERAL\n"
		t=t+"* Hold Left/Right Mouse - Adds/removes tiles.\n"
		t=t+"* Hold Spacebar - Opens up the Tile Selector.\n"
		t=t+"\n"
		t=t+"TILE SELECTOR\n"
		t=t+"* Hold and Drag Left Mouse - Select tiles.\n"
		t=t+"* Select Dropdown item - Change tilesheet.\n"
		t=t+"\n\n---\n\n"
		t=t+"TIPS\n"
		_="* A single Room cannot use more than %s different tilesheets.\n"\
		% c
		t=t+_
		t=t+"* A cursor with a lot of tiles can be used as a HUGE eraser.\n"
		self.help_text = t


	def normal_draw(self, target, states):
		#Cursor
		if not self.Selector.opened and self.active\
		and not self.parent_states.hovered:
			self.Cursor.draw(target, states)

	def static_draw(self, target, states):
		#Selector
		target.draw(self.Selector, states)
		_Tool.static_draw(self, target, states)

	#

	def add_controls(self, WorldMap):
		if not self.active: return
		Key, Mouse, Camera = self._Key, self._Mouse, self._Camera
		if not self.parent_states.hovered:
			self._control_Cursor(Key, Mouse, Camera, WorldMap)
		self._control_Selector(Key, Mouse, Camera)


	def open(self):
		_Tool.open(self)

	def close(self):
		_Tool.close(self)
		self.Selector.close()

	#################################
	# PRIVATE

	###
	#Cursor

	def _control_Cursor(self, Key, Mouse, Camera, WorldMap):

		#change tiles
		if not self.Selector.opened:
			self.Cursor.controls(Key, Mouse, Camera)
			if Mouse.left.held():
				self._change_tile(WorldMap)
			elif Mouse.right.held():
				self._change_tile(WorldMap, erase=True)

		#widen
		w = len(self.Selector.selected_tiles)-1
		h = len(self.Selector.selected_tiles[0])-1
		self.Cursor.tile_w = w
		self.Cursor.tile_h = h

	#

	def _change_tile(self, WorldMap, erase=False):
		#Change WorldMap tiles.

		#fits in map?
		x,y = self.Cursor.tile_position
		w = len(self.Selector.selected_tiles)
		h = len(self.Selector.selected_tiles[0])
		if not(0 <= x and x+w <= WorldMap.tile_w): return
		if not(0 <= y and y+h <= WorldMap.tile_h): return

		#create or erase
		if erase: texture = None
		else: texture = self.Selector.text

		#error text
		c = str(TILESHEET_CAP)
		t="Oh no!\n"
		t=t+"You've tried to add more than "+c+" tilesheets in one room.\n"
		t=t+"I'm sorry, but that's too many!\n"
		error_text = t
		del c; del t

		#change multi
		for ox in range(w):
			for oy in range(h):
				data = self.Selector.selected_tiles[ox][oy]
				cx,cy = int(data[:2]), int(data[2:])
				tile = WorldMap.tiles[x+ox][y+oy]

				#room has texture space
				if tile.room.has_slot_for_texture(texture)\
				or erase:
					tile.clip = cx,cy
					tile.texture = texture
				else:
					self.open_error = True
					self.error_text = error_text


	###
	#Selector

	def _control_Selector(self, Key, Mouse, Camera):
		if Key.SPACE.held():
			self.Selector.open()
			self.Selector.controls(Key, Mouse, Camera)
		else:
			self.Selector.close()


	class _Selector(Box):
		#A window for editing tiles.

		#################################
		# PUBLIC

		text = None

		@property
		def selected_tiles(self):
			return self.children[1].selected_tiles

		def __init__(self):
			Box.__init__(self)
			self.size = 550,275
			self._add_widgets()
		
		def controls(self, Key, Mouse, Camera):
			Box.controls(self, Key, Mouse, Camera)
			self._change_tilesheet()

		#################################
		# PRIVATE

		@property
		def text(self): return self._dropdown.text
		@text.setter
		def text(self, t): self._dropdown.text = t

		#

		def _add_widgets(self): #init
			#dropdown
			#grab
			def grab_list(directory):
				os.chdir(directory)
				l = []
				for files in os.listdir("."):
					if files.endswith(".png"):
						l.append(files[:-4])
					else:
						l.append([files]+grab_list(directory+"/"+files))
				return l

			old_dir = os.getcwd()
			l = grab_list(os.getcwd()+"/assets/tilesheets/")
			os.chdir(old_dir)
			#

			dropdown = Dropdown(l)
			dropdown.center = self.center
			dropdown.y = self.y2 - dropdown.h
			self.children.append(dropdown)
			self._dropdown = dropdown

			#tileselector
			tileselector = TileSelector(dropdown.text+".png")
			tileselector.tile_x += 1
			tileselector.tile_y += 1
			self.children.append(tileselector)
			self._tileselector = tileselector

		#

		_old_text = ""
		def _change_tilesheet(self): #controls
			if self._old_text != self._dropdown.text:
				self._tileselector.load(self._dropdown.text+".png")
			self._old_text = self._dropdown.text



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