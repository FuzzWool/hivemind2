from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
from code.level_editor.ui import UIBox, Dropdown

#######################################

from code.level_editor.ui import Grid

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