from code.sfml_plus import Rectangle
from code.sfml_plus.constants import ROOM_WIDTH
from code.sfml_plus.constants import ROOM_HEIGHT
from code.sfml_plus.constants import TILE

from sfml import VertexArray, PrimitiveType, RenderStates
from sfml import Texture
from sfml import Vertex
from sfml import Color


def Key(self, x,y): #unused
#data format for positioning.
	x,y = str(x),str(y)
	if len(x) == 1: "0"+x
	if len(y) == 1: "0"+y
	return x,y



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

	def __init__(self, x,y):
		self.room_position = x,y
		self.size = ROOM_WIDTH, ROOM_HEIGHT
		self._init_tiles()
		self._load_tiles(Tile)
		self._render_tiles()

	def draw(self, window):
		self._draw_tiles(window)


	#################################
	# PRIVATE

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
				tile = TileClass(x+ox, y+oy)
				self.tiles[x][y] = tile

	def _render_tiles(self): #init

		s = PrimitiveType.QUADS
		self.vertex_array = VertexArray(s)
		
		for column in self.tiles:
			for tile in column:
				tile.render()
				for point in tile.vertices:
					self.vertex_array.append(point)

		if self.room_position in [(0,0),(1,1)]:
			t = Texture.from_file("assets/tilesheets/0.png")
		else:
			t = Texture.from_file("assets/tilesheets/1.png")
		self.render_states = RenderStates()
		self.render_states.texture = t

	#

	def _draw_tiles(self, window): #WorldMap.draw
		window.draw(self.vertex_array, self.render_states)



class Tile(Rectangle):
# * Graphic - provides the tile to use in the sheet.
# It does not contain a graphic, rather, the clip to use.

	#################################
	# PUBLIC

	#Start
	def __init__(self, x,y):
		self.data = "0000"

		self.tile_position = x,y
		self.size = TILE, TILE

	#Room.render
	def render(self): self._create_vertices()

	#################################
	# PRIVATE

	# Start-up Sequence
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
		if not data == "____":
			clip_x = int(data[0:2])
			clip_y = int(data[2:4])

			x1 = (clip_x+0)*TILE
			y1 = (clip_y+0)*TILE
			x2 = (clip_x+1)*TILE
			y2 = (clip_y+1)*TILE

			point1.tex_coords = x1,y1
			point2.tex_coords = x2,y1
			point3.tex_coords = x2,y2
			point4.tex_coords = x1,y2

		else:
			for point in points:
				point.tex_coords = 0,0
				point.color = Color(0,0,0,0)

		for point in points:
			self.vertices.append(point)