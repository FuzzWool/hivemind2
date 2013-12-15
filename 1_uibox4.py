from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
from code.level_editor.ui import UIBox, Dropdown

#######################################

from code.level_editor.ui import Grid
from code.level_editor.ui import _UI

from code.sfml_plus import Rectangle
from code.sfml_plus import MySprite
from sfml import Texture
from sfml import Color


class TileSelector(_UI):
# WIP - Selects tiles on a Tilesheet.
	# WIP - May store multiple tiles.

	x,y,w,h = 0,0,0,0
	graphics = []

	def __init__(self):
		self.Tileset = self.Tileset("1")
		self.New_Cursor = self.Cursor()
		self.Old_Cursor = self.Cursor()
		self.size = self.Tileset.size
		self.Old_Cursor.skin = 1
		self.old_pos = self.position


	old_pos = 0,0
	def update_graphics(self):
		self.Tileset.position =self.position
		x = self.x - self.old_pos[0]
		y = self.y - self.old_pos[1]
		self.Old_Cursor.x +=x; self.Old_Cursor.y +=y
		self.New_Cursor.x +=x; self.New_Cursor.y +=y
		self.old_pos = self.position

		graphics = self.Tileset.graphics
		graphics += [self.Old_Cursor]
		graphics += [self.New_Cursor]
		self.graphics = graphics


	def controls(self, Key, Mouse, Camera):
		self.New_Cursor.active =Mouse.inside(self.Tileset)
		self.New_Cursor.controls(Mouse)

		selecting = self.New_Cursor.selecting
		if selecting:
			self.Old_Cursor.active =True
			self.Old_Cursor.tile_position \
			=self.New_Cursor.tile_position
			self.Old_Cursor.tile_size \
			=self.New_Cursor.tile_size


	def draw(self, Window):
		self.Tileset.draw(Window)
		self.Old_Cursor.draw(Window)
		self.New_Cursor.draw(Window)


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
		def _make_sprite(self, path): #init
			texture = Texture.from_file(path)
			sprite = MySprite(texture)
			self.size = sprite.size
			self.sprite = sprite

		grid = None
		def _make_grid(self): #init
			self.grid = Grid(self.points)



	class Cursor(Rectangle):
	#A cursor sprite.
	#
	# * Edges are split into 4 parts for multi-selections.
	# * It snaps to the mouse tile-per-tile.
	# * Handles tile selections.

		active = False
		selecting = False
		skin = 0 #0,1


		#COLOR
		#Forcefully dumbs down the alpha for UIBox.

		_color = Color(255,255,255,50)
		@property
		def color(self): return self._color
		@color.setter
		def color(self,color):
			if self.skin == 1: color.a /= 2
			for row in self.sprites:
				for sprite in row:
					sprite.color = color

			self._color = color
		#


		# @property
		# def selected(self): #unused, returns a 2D list
		# 	pass

		def __init__(self):
			self.sprites = self._make_sprites()

		def controls(self, Mouse):
			if not self.active: return
			
			self.tile_position = Mouse.tile_position
			self._select_tiles(Mouse)

		def draw(self, Window):
			if not self.active: return

			self.sprites = self._position_sprites()
			for row in self.sprites:
				for sprite in row:
					Window.draw(sprite)

		@property
		def graphics(self):
			graphics = []
			for row in self.sprites:
				for sprite in row:
					graphics.append(sprite)
			return graphics

		########################################

		sprites = []
		tex_path = "assets/ui/cursor.png"
		texture = Texture.from_file(tex_path)

		def _make_sprites(self): #init
			sprites = []
			texture = self.texture
			w,h = self.size
			#
			for x in range(2):
				sprites.append([])
				for y in range(2):
					sprite = MySprite(texture)
					sprite.clip.set(8,8)
					sprite.clip.use(x*2,y*2)

					o = sprite.origin
					if x > 0: sprite.origin = -16,o[1]
					o = sprite.origin
					if y > 0: sprite.origin = o[0],-16

					sprites[-1].append(sprite)
			#
			return sprites


		def _position_sprites(self): #draw
			sprites = self.sprites
			x1,y1,x2,y2 = self.points
			#
			sprites[0][0].position = x1,y1
			sprites[0][1].position = x1,y2
			sprites[1][0].position = x2,y1
			sprites[1][1].position = x2,y2
			#
			return sprites

		#

		selecting = False
		start_anchor = 0,0
		finish_anchor = 0,0
		#
		def _select_tiles(self, Mouse): #controls
			_x,_y = self.tile_position
			tile_points = _x,_y,_x+1,_y+1
			#
			selecting = self.selecting
			start_anchor = self.start_anchor
			finish_anchor = self.finish_anchor
			#
			if Mouse.left.held() and (not selecting):
				selecting = True
				start_anchor = tile_points[0:2]
			if selecting:
				finish_anchor = tile_points[2:4]
			if (not Mouse.left.held()) and selecting:
				selecting = False
			#
			self.selecting = selecting
			self.start_anchor = start_anchor
			self.finish_anchor = finish_anchor
			#
			if selecting:
				x,y = start_anchor
				w = finish_anchor[0]-start_anchor[0]-1
				h = finish_anchor[1]-start_anchor[1]-1
				if w < 0: x += w; w = abs(w)
				if h < 0: y += h; h = abs(h)
				self.tile_position = x,y
				self.tile_size = w,h
			else:
				self.tile_size = 0,0

		#


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