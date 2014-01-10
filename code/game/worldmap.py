from code.sfml_plus import Rectangle
from code.sfml_plus.constants import ROOM_WIDTH
from code.sfml_plus.constants import ROOM_HEIGHT
from code.sfml_plus.constants import TILE

from sfml import VertexArray, PrimitiveType, RenderStates
from sfml import Texture
from sfml import Vertex
from sfml import Color


def Key(x,y): #unused
#data format for positioning.
	x,y = str(x),str(y)
	if len(x) == 1: x = "0"+x
	if len(y) == 1: y = "0"+y
	return x+y



class WorldMap(Rectangle):
# * contains all of the Rooms, which then contain Tiles.

	#################################
	# PUBLIC

	tiles = []

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

	#################################
	# PRIVATE

	#Accessing
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


	#Loading
	def _init_rooms(self, w,h):
		self.rooms = []
		for x in range(w):
			self.rooms.append([])
			for y in range(h):
				self.rooms[-1].append(None)

	def _load_rooms(self, RoomClass):
		for x, column in enumerate(self.rooms):
			for y, _room in enumerate(column):
				room = RoomClass(x,y)
				self.rooms[x][y] = room





class Room(Rectangle):
# * contains all of the Tiles.
# * Graphic - in charge of generating a vertex array.

	#################################
	# PUBLIC

	tiles = []

	def __init__(self, x,y):
		self.child = self.child()
		self.room_position = x,y
		self.size = ROOM_WIDTH, ROOM_HEIGHT
		self._init_tiles()
		self._load_tiles(Tile)

		self._init_render()
		self._init_textures()
		self._render_tiles()

	def draw(self, window):
		self._parent_tiles()
		self._draw_tiles(window)


	#################################
	# PRIVATE


	TILESHEET_CAP = 5
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
				tile = TileClass(x+ox, y+oy, self.child)
				self.tiles[x][y] = tile


	###
	# RENDERING

	_vertex_arrays = []

	def _init_render(self):

		self._vertex_arrays = []
		s = PrimitiveType.QUADS
		for i in range(self.TILESHEET_CAP):
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
					if tile.data[0] == "_":
						pass
					else:
						no = int(tile.data[0])
						self._vertex_arrays[no].append(point)


	def _draw_tiles(self, window): #WorldMap.draw
		for i, _s in enumerate(self._vertex_arrays):
			window.draw(self._vertex_arrays[i], self._render_states[i])



	###
	# Textures

	_texture_slots = [None, None, None, None, None]

	def _init_textures(self): #init
		self._render_states = []
		for i in range(self.TILESHEET_CAP):
			self._render_states.append(RenderStates())
			s = "_default/%s.png" % str(i)
			t = Texture.from_file("assets/tilesheets/"+s)
			self._render_states[-1].texture = t

		self._texture_slots = [None for i in range(self.TILESHEET_CAP)]


	def _update_textures(self): #_init_textures, parent_tiles

		#Find all current textures.
		textures = []
		for column in self.tiles:
			for tile in column:
				if tile.texture not in textures:
					textures.append(tile.texture)

		#Remove any old, non-existing textures.
		for slot_i, slot in enumerate(self._texture_slots):
			texture_found = False
			for texture in textures:
				if slot == texture:
					texture_found = True
			if not texture_found:
				self._texture_slots[slot_i] = None

		#Add any newly appeared textures.
		for texture in textures:
			#new texture found
			if texture not in self._texture_slots:
				slot_found = False
				for slot_i, slot in enumerate(self._texture_slots):
					#free slot
					if slot == None:
						self._texture_slots[slot_i] = texture
						slot_found = True
						break
				#all slots filled
				if not slot_found:
					raise "No space for a new texture!"


		#Update state textures for drawing.
		pass


		if self.position == (0,0):
			print textures
			print self._texture_slots




	###
	# Parent


	def _parent_tiles(self):
		if self.child.render_request: self._render_tiles()
		self.child.render_request = False
		#
		if self.child.texture_request: self._update_textures()
		self.child.texture_request = False

	class child:
		render_request = False
		texture_request = False



class Tile(Rectangle):
# * Graphic - provides the tile to use in the sheet.
# It does not contain a graphic, rather, the clip to use.

	#################################
	# PUBLIC

	# clip = 0,0
	texture = ""

	def __init__(self, x,y, parent):
		self.parent = parent
		self.data = "00000" #tilesheet/position

		self.tile_position = x,y
		self.size = TILE, TILE
		self.texture = "_default/0"

	def render(self): self._create_vertices()


	#################################
	# PRIVATE


	###
	# Parent

	_texture = ""
	@property
	def texture(self): return self._texture
	@texture.setter
	def texture(self, texture):
		self._texture = texture
		self.parent.texture_request = True


	_data = "00000"
	@property
	def data(self): return self._data
	@data.setter
	def data(self,d):
		self._data = d
		self.parent.render_request = True



	###
	# Init

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
		data = self.data
		if data == "_____":
			for point in points:
				point.tex_coords = 0,0
				point.color = Color(0,0,0,0)
		else:
			# sheet = int(data[0])
			clip_x = int(data[1:3])
			clip_y = int(data[3:5])

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