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
from code.sfml_plus.constants import TILE

class TileSelector(_UI):
# WIP - Selects tiles on a Tilesheet.
	# WIP - May store multiple tiles.

	x,y,w,h = 0,0,0,0
	graphics = []


	def __init__(self):
		self.Tileset = self.Tileset("1")
		self.Cursor = self.Cursor()
		self.size = self.Tileset.size

	def controls(self, Key, Mouse, Camera):
		self.Cursor.active = Mouse.inside(self.Tileset)
		self.Cursor.controls(Mouse)

	def update_graphics(self):
		self.Tileset.position = self.position
		self.graphics = self.Tileset.graphics

	def draw(self, Window):
		self.Tileset.draw(Window)
		self.Cursor.draw(Window)


	#######################################

	class Tileset(Rectangle):
	#A tileset image with a grid overlaying it.

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
	#A cursor sprite.
	#Each edge is split into 8 parts for multi-selections.
	#It snaps to the mouse tile-per-tile.	

		active = False

		def __init__(self):
			self.sprites = self._make_sprites()

		def controls(self, Mouse):
			if not self.active: return
			self.tile_position = Mouse.tile_position
			self.sprites = self._position_sprites()

		def draw(self, Window):
			if not self.active: return
			for row in self.sprites:
				for sprite in row:
					Window.draw(sprite)

		########################################

		sprites = []
		tile_x, tile_y = 0,0
		w,h = TILE, TILE
		tex_path = "assets/ui/cursor.png"
		texture = Texture.from_file(tex_path)

		def _make_sprites(self): #init
			sprites = []
			texture = self.texture
			w,h = self.size
			#
			for x in range(3):
				sprites.append([])
				for y in range(3):
					sprite = MySprite(texture)
					sprite.clip.set(8,8)
					sprite.clip.use(x,y)

					o = sprite.origin
					if x > 0: sprite.origin = -8*x,o[1]
					o = sprite.origin
					if y > 0: sprite.origin = o[0],-8*y

					sprites[-1].append(sprite)
			#
			return sprites


		def _position_sprites(self): #snap_to
			sprites = self.sprites
			tile_position = self.tile_position
			#
			for row in sprites:
				for sprite in row:
					sprite.tile_position = tile_position
			#
			return sprites


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