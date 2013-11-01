from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((600,300), "Hivemind - Demo 2")

################################################

class WorldMap:
# * WIP - contains Rooms filled with tiles.
# * WIP - contains Tiles of all the (active) rooms.

	#Start-up Sequence
	def __init__(self, w,h):
		self._init(w,h)

	def _init(self, w,h):
		self.rooms = []
		for x in range(w):
			self.rooms.append([])
			for y in range(h):
				self.rooms[-1].append(None)

	def _load(self):
		pass

	def _render(self):
		pass
	#

	def draw(self):
		pass



class Room:
# * WIP - contains all of the Tiles.
# * WIP- render - in charge of generating a vertice array.

	# Start-up Sequence
	def __init__(self):
		pass

	def _init(self):
		pass

	def _load(self):
		pass

	def _render(self):
		pass
	#
	
	def draw(self):
		pass


class Tile:
# * WIP- Graphic - provides the tile to use in the sheet.
# It does not contain a graphic, rather, the clip to use.
		
	# Start-up Sequence
	def __init__(self):
		pass

	def _init(self):
		pass

	def _load(self):
		pass

	def _render(self):
		pass
	#

	def draw(self):
		pass



################################################

while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed(): print 1

	window.clear((255,220,0))
	window.display()