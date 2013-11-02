from code.sfml_plus import Rectangle
ROOM_WIDTH, ROOM_HEIGHT = 600,300
TILE = 25
#
from sfml import VertexArray, PrimitiveType, RenderStates
from sfml import Texture
from sfml import Vertex
from sfml import Color

class WorldMap(Rectangle):
# * contains Rooms filled with tiles.
# * WIP - contains Tiles of all the (active) rooms.

	#Start-up Sequence
	def __init__(self, w,h):
		self.room_size = w,h
		self._init(w,h)
		self._load()

	def _init(self, w,h): #init
		self.rooms = []
		for x in range(w):
			self.rooms.append([])
			for y in range(h):
				self.rooms[-1].append(None)

	def _load(self): #init
		for x, column in enumerate(self.rooms):
			for y, _room in enumerate(column):
				room = Room(x,y)
				self.rooms[x][y] = room


	def _render(self):
		pass
	#

	def draw(self, window):
		for column in self.rooms:
			for room in column:
				room.draw(window)


class Room(Rectangle): #WorldMap
# * contains all of the Tiles.
# * WIP- render - in charge of generating a vertex array.

	# Start-up Sequence
	def __init__(self, x,y):
		self.room_position = x,y
		self.size = ROOM_WIDTH, ROOM_HEIGHT
		self._init()
		self._load()
		self._render()

	def _init(self): #init
		tiles = []
		w, h = self.tile_size
		for x in range(w):
			tiles.append([])
			for y in range(h):
				tiles[-1].append([])

		self.tiles = tiles

	def _load(self): #init
		self.tiles
		ox, oy = self.tile_position
		for x, column in enumerate(self.tiles):
			for y, _tile in enumerate(column):
				tile = Tile(x+ox, y+oy)
				self.tiles[x][y] = tile

	def _render(self): #init

		s = PrimitiveType.QUADS
		self.vertex_array = VertexArray(s)
		
		for column in self.tiles:
			for tile in column:
				tile.render()
				for point in tile.vertices:
					self.vertex_array.append(point)

		if self.room_position in [(0,0),(1,1)]:
			t = Texture.from_file("assets/tilesets/1.png")
		else:
			t = Texture.from_file("assets/tilesets/2.png")
		self.render_states = RenderStates()
		self.render_states.texture = t

	#
	
	def draw(self, window): #WorldMap.draw
		window.draw(self.vertex_array, self.render_states)


class Tile(Rectangle): #Room
# * WIP- Graphic - provides the tile to use in the sheet.
# It does not contain a graphic, rather, the clip to use.
		
	# Start-up Sequence

	def __init__(self, x,y):
		self.tile_position = x,y
		self.size = TILE, TILE
		self._init()
		self._load()

	def _init(self): #init
		self.data = ""

	def _load(self): #init
		self.data = "0000"

	def render(self): #Room.render
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
	#

	def draw(self):
		pass #Handled by Room.draw