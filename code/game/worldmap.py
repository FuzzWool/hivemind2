from _worldmap import _WorldMap, _Room, _Tile
ROOM_WIDTH, ROOM_HEIGHT = 600,300
TILE = 25

class WorldMap(_WorldMap):
# * contains all of the Rooms, which then contain Tiles.

	#Start
	def __init__(self, w,h):
		self.room_size = w,h
		self._init(w,h)
		self._load()

	def _init(self, w,h): self._init_rooms(w,h)
	def _load(self): self._load_rooms(Room)

	#Loop
	def _render(self): pass

	def draw(self, window):
		for column in self.rooms:
			for room in column:
				room.draw(window)


class Room(_Room):
# * contains all of the Tiles.
# * Graphic - in charge of generating a vertex array.

	#Start
	def __init__(self, x,y):
		self.room_position = x,y
		self.size = ROOM_WIDTH, ROOM_HEIGHT
		self._init()
		self._load()
		self._render()

	def _init(self): self._init_tiles()
	def _load(self): self._load_tiles(Tile)
	def _render(self): self._render_tiles()
	#

	#Loop
	def draw(self, window): self._draw_tiles(window)


class Tile(_Tile):
# * Graphic - provides the tile to use in the sheet.
# It does not contain a graphic, rather, the clip to use.

	#Start
	def __init__(self, x,y):
		self.data = "0000"

		self.tile_position = x,y
		self.size = TILE, TILE

	def _init(self): pass
	def _load(self): pass
	#

	#Room.render
	def render(self): self.create_vertices()

	#
	
	def draw(self): pass