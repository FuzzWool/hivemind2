from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
from code.level_editor.ui import UIBox, Dropdown

#######################################

from code.sfml_plus import Rectangle
from sfml import RectangleShape
from sfml import Color
from code.sfml_plus.constants import TILE

class Grid(Rectangle):
#Create a grid around a rectangle.

	graphics = []	
	horizontal_lines = []
	vertical_lines = []

	def __init__(self, points):
		self.points = points

	old_points = 0,0,0,0
	def draw(self, Window):
		if self.old_points != self.points:
			self._make_lines()
		self.old_points = self.points

		for line in self.vertical_lines:
			Window.draw(line)
		for line in self.horizontal_lines:
			Window.draw(line)


	#COLOR
	#Always keep the color transparent.

	_color = Color(0,0,0,50)
	@property
	def color(self): return self._color
	@color.setter
	def color(self,color):
		color.a /= 5
		self._color = color
		self._make_lines()

	#

	def _make_lines(self): #draw
		pos = self.position
		color = self.color
		w,h = self.tile_size
		x,y = 0,0
		vertical_lines = []
		horizontal_lines = []
		#
		for x in range(w+1):
			line = RectangleShape((0,h*TILE))
			line.position = pos[0]+x*TILE,pos[1]
			line.outline_thickness = 1
			line.outline_color = color
			vertical_lines.append(line)
		for y in range(h+1):
			line = RectangleShape((w*TILE,0))
			line.position = pos[0],pos[1]+y*TILE
			line.outline_thickness = 1
			line.outline_color = color
			horizontal_lines.append(line)
		#
		self.vertical_lines = vertical_lines
		self.horizontal_lines = horizontal_lines
		#
		self.graphics = []
		for line in self.vertical_lines:
			self.graphics.append(line)
		for line in self.horizontal_lines:
			self.graphics.append(line)







from code.level_editor.ui import _UI
from code.sfml_plus import Rectangle
from sfml import Texture
from code.sfml_plus import MySprite

class TileSelector(_UI):
# WIP - Selects tiles on a Tilesheet.
	# WIP - May store multiple tiles.

	x,y,w,h = 0,0,0,0
	graphics = []


	def __init__(self):
		self.Tileset = self.Tileset("1")
		self.size = self.Tileset.size

	def controls(self, Key, Mouse, Camera):
		pass

	def update_graphics(self):
		self.Tileset.position = self.position
		self.graphics = self.Tileset.graphics

	def draw(self, Window):
		self.Tileset.draw(Window)


	#######################################

	class Tileset(Rectangle):
		
		def __init__(self, path):
			self.load(path)

		def load(self, path):
			path = "assets/tilesets/%s.png" % path
			self._make_sprite(path)
			self._make_grid()

		def draw(self, Window):
			self.sprite.position = self.position
			self.grid.position = self.position
			Window.draw(self.sprite)
			self.grid.draw(Window)

		@property
		def graphics(self):
			return [self.sprite] + [self.grid]

		###################################

		sprite = None
		def _make_sprite(self, path):
			texture = Texture.from_file(path)
			sprite = MySprite(texture)
			self.size = sprite.size
			self.sprite = sprite

		grid = None
		def _make_grid(self):
			self.grid = Grid(self.points)

	class Cursor(Rectangle):
		pass



#######################################

Window = Window((1200,600), "UI Box (Tile)")

UIBox1 = UIBox()
UIBox1.size = 550,250
UIBox1.center = Window.center
UIBox1.open()

dropdown = Dropdown\
(["a",["A","aa",["C","ca"]],["B","ba",["D","da"]]])
dropdown.center = UIBox1.center
dropdown.y = UIBox1.y2 - dropdown.h
UIBox1.add(dropdown)


tileselector = TileSelector()
tileselector.center = UIBox1.center
UIBox1.add(tileselector)

Mouse = Mouse(Window)

while Window.is_open:

	if Window.is_focused:
		UIBox1.controls(Key, Mouse, None)

		if Key.ENTER.pressed():
			UIBox1.center = Window.center
			UIBox1.open()
		if Key.BACKSPACE.pressed():
			UIBox1.close()

	Window.clear((255,220,0))
	UIBox1.draw(Window)
	Window.display(Mouse)