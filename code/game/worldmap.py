from _worldmap import _WorldMap, _Room, _Tile
from code.sfml_plus.constants import ROOM_WIDTH
from code.sfml_plus.constants import ROOM_HEIGHT
from code.sfml_plus.constants import TILE

class WorldMap(_WorldMap):
# * contains all of the Rooms, which then contain Tiles.

	tiles = [] #@property

	#

	#Start
	def __init__(self, w,h):
		self.room_size = w,h
		self._init(w,h)
		self._load()

	def _init(self, w,h): self._init_rooms(w,h)
	def _load(self): self._load_rooms(Room)

	#Loop
	def _render(self): pass

	def draw(self, window, camera):
		x1,y1,x2,y2 = camera.room_points
		x2+=2; y2+=2
		p = self.room_points
		x1,y1 = camera.keep_in_points((x1,y1),p)
		x2,y2 = camera.keep_in_points((x2,y2),p)

		for column in self.rooms[x1:x2]:
			for room in column[y1:y2]:
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