from code.sfml_plus import Rectangle
from code.sfml_plus.constants import ROOM_WIDTH
from code.sfml_plus.constants import ROOM_HEIGHT
from code.sfml_plus.constants import TILE

from sfml import VertexArray, PrimitiveType, RenderStates
from sfml import Texture
from sfml import Vertex
from sfml import Color

#Room.Grid
from code.sfml_plus import Grid_Room

#Saving/Loading
import os

#

TILESHEET_CAP = 5

def Key(x,y):
#Data format for tile positioning.
	x,y = str(x),str(y)
	if len(x) == 1: x = "0"+x
	if len(y) == 1: y = "0"+y
	return x+y

def Big_Key(x,y):
#Triple digits, for potentially huge, huge maps.
	x,y = str(x),str(y)
	if len(x) == 1: x = "00"+x
	if len(y) == 1: y = "00"+y
	if len(x) == 2: x = "0"+x
	if len(y) == 2: y = "0"+y
	return x+y

#

class WorldMap(Rectangle):
# contains all of the Rooms, which then contain Tiles.
# * saves and loads entire map files.

	#################################
	# PUBLIC

	tiles = []
	enable_grid = True

	error = None

	def __init__(self, w,h):
		self.room_size = w,h
		self._init_rooms(w,h)
		self._load_rooms(Room)
		self._tile_access()

	def draw(self, window, camera):
		x1,y1,x2,y2 = camera.room_points
		x2+=2; y2+=2
		p = self.room_points
		x1,y1 = camera.keep_in_points((x1,y1),p)
		x2,y2 = camera.keep_in_points((x2,y2),p)

		for column in self.rooms[x1:x2]:
			for room in column[y1:y2]:
				room.draw(window)
				if self.enable_grid:
					room.draw_grid(window)

	#

	def save(self, map_name):
		self._save(map_name)
	def load(self, map_name):
		self._load(map_name)


	#################################
	# PRIVATE

	###
	# Accessing

	def _tile_access(self):
		self.tiles = []
		#Grab every ROOM in a COLUMN.
		for room_x in self.rooms:
			#For every TILE COLUMN...
			tile_w = len(room_x[0].tiles)
			for tile_x in range(tile_w):
				#...grab it from all the ROOMS,
				# and connect them.
				column = []
				for room_y in room_x:
						column += room_y.tiles[tile_x]
				
				self.tiles.append(column)

	###
	# Loading

	def _init_rooms(self, w,h):
		self.rooms = []
		for x in range(w):
			self.rooms.append([])
			for y in range(h):
				self.rooms[-1].append(None)

	def _load_rooms(self, RoomClass):
		for x, column in enumerate(self.rooms):
			for y, _room in enumerate(column):
				self.rooms[x][y] = RoomClass(x,y)


	###
	# Saving/Loading

	def _save(self, map_name):

		# Make Map folder (if needed)
		mypath = os.getcwd()
		if not os.path.isdir(mypath+"\maps\\"+map_name):
			os.makedirs(mypath+"\maps\\"+map_name)

		# Make a .txt file for each room
		for column in self.rooms:
			for room in column:
				_name = Big_Key(*room.room_position)
				f = open(mypath+"\maps\\"+map_name+"\\"+_name+".txt", "w+")
				#
				# Header: texture slots, Footer: texture/clipx/clipy tiles
				_t = str(room.texture_slots)
				for tcolumn in room.tiles:
					_t = _t+"\n"
					for tile in tcolumn:
						_t = _t+tile.data
				f.write(_t)
				f.close()


	def _load(self, map_name):

		#Load data for every room.
		for column in self.rooms:
			for room in column:
				_k = Big_Key(*room.room_position)
				f = open("maps/"+map_name+"/"+_k+".txt", "r")
				#
				_f = f.read().split("\n")
				
				#Grab and seperate header and body
				_f[0] = _f[0].translate(None, "'")
				_f[0] = _f[0].translate(None, " ")
				header = _f[0][1:-1].split(",")
				body = []
				for _fl in _f[1:]:
					body.append([_fl[i:i+5] for i in range(0,len(_fl),5)])

				#Apply data to each tile.
				for ix, tcolumn in enumerate(room.tiles):
					for iy, tile in enumerate(tcolumn):
						_tex = body[ix][iy][0]
						if _tex == "_":
							tile.texture = None
							tile.clip = 0,0
						else:
							tile.texture = header[int(_tex)]
							x = int(body[ix][iy][1:3])
							y = int(body[ix][iy][3:6])
							tile.clip = x,y
				#
				f.close()





######################################################################
######################################################################
######################################################################


class Room(Rectangle):
# * contains all of the Tiles.
# * Graphic - in charge of generating a vertex array.
# * Logic - communicates rendering and texturing requests with Tiles.

	#################################
	# PUBLIC

	tiles = []
	has_slot_for_texture = None

	def __init__(self, x,y):
		self.child_listen = self.child_listen()
		self.child_tell = self.child_tell()

		self.room_position = x,y
		self.size = ROOM_WIDTH, ROOM_HEIGHT
		self._init_tiles()
		self._load_tiles(Tile)
		self._init_render()
		self._init_textures()
		self._render_tiles()

		self._create_Grid()

	def draw(self, window):
		self._child_listening()
		self._draw_tiles(window)

	def draw_grid(self, window):
		self._draw_Grid(window)


	#################################
	# PRIVATE

	#TILESHEET_CAP
	texture_slots = [None, None, None, None, None] #readonly
	_render_states = []


	###
	# TILES

	def _init_tiles(self): #init
		tiles = []
		w, h = self.tile_size
		for x in range(w):
			tiles.append([])
			for y in range(h):
				tiles[-1].append([])

		self.tiles = tiles

	def _load_tiles(self, TileClass): #init
		self.tiles
		ox, oy = self.tile_position
		for x, column in enumerate(self.tiles):
			for y, _tile in enumerate(column):
				tile = TileClass(x+ox, y+oy,
						self.child_tell, self.child_listen, self)
				self.tiles[x][y] = tile


	###
	# RENDERING

	_vertex_arrays = []

	def _init_render(self):

		self._vertex_arrays = []
		s = PrimitiveType.QUADS
		for i in range(TILESHEET_CAP):
			self._vertex_arrays.append(VertexArray(s))


	def _render_tiles(self): #init, _parent_tiles
		
		#clear arrays
		for array in self._vertex_arrays:
			array.clear()

		#append arrays
		for column in self.tiles:
			for tile in column:
				tile.render()
				for point in tile.vertices:
					
					#choose array (texture)
					if tile.texture != None:
						no = int(tile.data[0])
						self._vertex_arrays[no].append(point)


	def _draw_tiles(self, window): #WorldMap.draw
		for i, _s in enumerate(self._vertex_arrays):
			window.draw(self._vertex_arrays[i], self._render_states[i])



	###
	# Textures
	#! child_tell.texture_slots dependancy

	def has_slot_for_texture(self, checked_texture):
		for texture in self.texture_slots:
			if texture == None: return True
			if texture == checked_texture: return True
		return False

	#

	def _init_textures(self): #init
		self._render_states = []
		for i in range(TILESHEET_CAP):
			self._render_states.append(RenderStates())

		self.texture_slots = [None for i in range(TILESHEET_CAP)]
		self.texture_slots[0] = None
		self.child_tell.texture_slots = self.texture_slots


	def _update_textures(self): #_child_listening

		#Find all current textures.
		textures = []
		for column in self.tiles:
			for tile in column:
				if tile.texture not in textures:
					textures.append(tile.texture)

		#Remove any old, non-existing textures.
		for slot_i, slot in enumerate(self.texture_slots):
			texture_found = False
			for texture in textures:
				if slot == texture:
					texture_found = True
			if not texture_found:
				self.texture_slots[slot_i] = None

		#Add any newly appeared textures.
		for texture in textures:
			#new texture found
			if texture not in self.texture_slots:
				slot_found = False
				for slot_i, slot in enumerate(self.texture_slots):
					#free slot
					if slot == None:
						self.texture_slots[slot_i] = texture
						slot_found = True
						break
				# #all slots filled
				# if not slot_found:
				# 	pass

		#Update state textures for drawing.
		for i in range(TILESHEET_CAP):
			texture = self.texture_slots[i]
			if texture != None:
				t = "assets/tilesheets/"+texture+".png"
				self._render_states[i].texture = Texture.from_file(t)

		#Tell children, for their data, what slot their texture uses.
		self.child_listen.texture_slots = self.texture_slots


	###
	# Child Listening/Telling

	def _child_listening(self):
		if self.child_listen.texture_request: self._update_textures()
		self.child_listen.texture_request = False
		#
		if self.child_listen.render_request: self._render_tiles()
		self.child_listen.render_request = False

	class child_listen:
		render_request = False
		texture_request = False

	class child_tell:
		texture_slots = [None,None,None,None,None]


	###
	# Grid

	_Grid = None

	def _create_Grid(self):
		self._Grid = Grid_Room()
		self._Grid.position = self.position

	def _draw_Grid(self, Window):
		Window.draw(self._Grid)


######################################################################
######################################################################
######################################################################


class Tile(Rectangle):
# * Graphic - provides the tile to use in the sheet.
# It does not contain a graphic, rather, the clip to use.

	#################################
	# PUBLIC

	clip = 0,0
	texture = ""
	room = None

	def __init__(self, x,y, parent_listen, parent_tell, room):

		self.room = room
		self.parent_listen = parent_listen
		self.parent_tell = parent_tell
		self.tile_position = x,y
		self.size = TILE, TILE

		#testing
		self.texture = None
		self.clip = 0,0

	def render(self): self._create_vertices()


	#################################
	# PRIVATE

	###
	# Tile Data (Parent tell, listen)

	_texture = ""
	_clip = 0,0
	
	@property
	def texture(self): return self._texture
	@texture.setter
	def texture(self, texture):
		if self._texture != texture:
			self._texture = texture
			self.parent_tell.texture_request = True
			self.parent_tell.render_request = True

	@property
	def clip(self): return self._clip
	@clip.setter
	def clip(self, pos):
		if self._clip != pos:
			self._clip = pos
			self.parent_tell.render_request = True
	
	@property
	def data(self):
		if self.texture == None:
			t = "_"
		else:
			t = str(self.parent_listen.texture_slots.index(self._texture))
		x,y = str(self.clip[0]),str(self.clip[1])
		if len(x) == 1: x = "0"+x
		if len(y) == 1: y = "0"+y
		return t+x+y



	###
	# Draw Position, Texture

	def _create_vertices(self): #Room.render
		self.vertices = []

		#points
		point1 = Vertex()
		point2 = Vertex()
		point3 = Vertex()
		point4 = Vertex()
		points = [point1,point2,point3,point4]

		#position
		x1, y1, x2, y2 = self.points
		point1.position = x1,y1
		point2.position = x2,y1
		point3.position = x2,y2
		point4.position = x1,y2

		#clip
		if self.texture == None:
			for point in points:
				point.tex_coords = 0,0
				point.color = Color(0,0,0,0)
		else:
			clip_x, clip_y = self.clip

			x1 = (clip_x+0)*TILE
			y1 = (clip_y+0)*TILE
			x2 = (clip_x+1)*TILE
			y2 = (clip_y+1)*TILE

			point1.tex_coords = x1,y1
			point2.tex_coords = x2,y1
			point3.tex_coords = x2,y2
			point4.tex_coords = x1,y2

		for point in points:
			self.vertices.append(point)