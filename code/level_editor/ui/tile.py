from code.sfml_plus.ui import Box
from code.sfml_plus import Texture, MySprite
from code.sfml_plus import Rectangle
from code.sfml_plus import Grid
from code.sfml_plus.constants import TILE

#Tile
from code.game.worldmap import Key as MapKey
from sfml import Color

class TileSelector(Box):
	
	#################################
	# PUBLIC

	selected_tiles = [["0000"]]

	def __init__(self,texture):
		self.selected_tiles = [["0000"]]
		#
		Box.__init__(self)
		self.Sheet = self.Sheet(texture)
		self.size = self.Sheet.size
		self.Grid = Grid(*self.size)
		self.Cursor = Cursor()
		self.Old_Cursor = Cursor()

	def controls(self, Key, Mouse, Camera):
		self._control_Cursor(Key, Mouse, Camera)
		if self.Cursor.selected:
			self.Old_Cursor.position = self.Cursor.position
			self.Old_Cursor.size = self.Cursor.size

	def draw(self, target, states):
		self._parent_Graphics()
		Box.draw(self, target, states)
		self.Sheet.draw(target, states)
		target.draw(self.Grid)
		self._draw_Cursor(target, states)

	#

	def load(self,texture):
		self.Sheet.change_sprite("assets/tilesheets/"+texture)

	#################################
	# PRIVATE

	# GRAPHICS
	def _parent_Graphics(self):
		c=self.Grid.color;c.a=self.alpha/4;self.Grid.color=c
		self.Grid.position = self.position
		#
		self.Sheet.alpha = self.alpha
		self.Sheet.position = self.position
		#

		def update_cursors(cursor, div=1):
			c=cursor.color;c.a=self.alpha/div;cursor.color=c
			x_move = self.x - self.old_pos[0]
			y_move = self.y - self.old_pos[1]
			cursor.x += x_move
			cursor.y += y_move
		#
		update_cursors(self.Cursor, 1)
		update_cursors(self.Old_Cursor, 2)

	# CURSOR

	_inside_sheet = False

	def _control_Cursor(self, Key, Mouse, Camera):
		self._inside_sheet = Mouse.inside(self.Sheet)
		if self._inside_sheet:
			self.Cursor.controls(Key, Mouse, Camera)

			#select tiles
			if self.Cursor.selected:
				x1 = self.Cursor.tile_x1 - self.tile_x
				y1 = self.Cursor.tile_y1 - self.tile_y
				x2 = self.Cursor.tile_x2 - self.tile_x
				y2 = self.Cursor.tile_y2 - self.tile_y

				#single
				# self.selected_tiles = [[MapKey(x1,y1)]]

				#multi
				self.selected_tiles = []
				for x in range(x1,x2+1):
					self.selected_tiles.append([])
					for y in range(y1,y2+1):
						self.selected_tiles[-1].append(MapKey(x,y))



	def _draw_Cursor(self, target, states):
		if self._inside_sheet:
			self.Cursor.draw(target, states)
		self.Old_Cursor.draw(target, states)


	# SHEET
	class Sheet(Rectangle):

		#################################
		# PUBLIC

		def __init__(self, name):
			Rectangle.__init__(self)
			self._create_sprite(name)

		def draw(self, target, states):
			self._parent_sprite()
			self._draw_sprite(target, states)
		#

		def change_sprite(self, texture):
			self._sprite.texture = Texture.from_file(texture)

		#################################
		# PRIVATE

		_sprite = None
		def _create_sprite(self, name):
			t = Texture.from_file("assets/tilesheets/"+name)
			self._sprite = MySprite(t)
			self.size = self._sprite.size
		#
		def _parent_sprite(self):
			c = self._sprite.color
			c.a = self.alpha
			self._sprite.color = c
			self._sprite.position = self.position
		def _draw_sprite(self, target, states):
			target.draw(self._sprite)







class Cursor(Rectangle):

	#################################
	# PUBLIC

	absolute = False
	expand = True
	color = Color(255,255,255,255)
	selected = False #readonly

	def __init__(self):
		self._create_corners()
		self.snap = True
		self.color = Color(255,255,255,255)
		self.expand = True
		self.selected = False
		self.absolute = False

	def controls(self, Key, Mouse, Camera):
		self._update_position(Mouse, Camera)
		if self.expand:
			self._expand(Mouse, Camera)

	def draw(self, target, states):
		self._update_corners_position()
		self._update_corners_alpha()
		self._draw_corners(target, states)

	#################################
	# PRIVATE

	# Position
	_selected = False

	def _update_position(self, Mouse, Camera):
		if not self._selected:
			self.tile_position = Mouse.tile_position
			self.tile_size = 0,0
			if self.absolute:
				self.tile_x = int(self.tile_x/Camera.zoom)
				self.tile_y = int(self.tile_y/Camera.zoom)
				self.tile_x += Camera.smooth.tile_x
				self.tile_y += Camera.smooth.tile_y

			if not Mouse.left.released():
				self.selected = False


	_start_anchor = 0,0
	_finish_anchor = 0,0
	def _expand(self, Mouse, Camera):
		#LOGIC
		#start
		if Mouse.left.pressed() and not self._selected:
			self._selected = True
			self._start_anchor = Mouse.tile_position
			if self.absolute:
				self._start_anchor[0] += Camera.tile_x
				self._start_anchor[1] += Camera.tile_y

		#loop
		if self._selected:
			self._finish_anchor = Mouse.tile_position
			if self.absolute:
				self._finish_anchor[0] += Camera.tile_x
				self._finish_anchor[1] += Camera.tile_y

		#reset
		self.selected = False
		if not Mouse.left.held():
			if self._selected: self.selected = True
			self._selected = False
			self._start_anchor = 0,0
			self._finish_anchor = 0,0

		#EFFECTS
		if self._selected:
			x1,y1,x2,y2 = self._start_anchor+self._finish_anchor
			if x1 > x2: x2,x1 = x1,x2
			if y1 > y2: y2,y1 = y1,y2
			self.tile_position = x1,y1
			self.tile_size = x2-x1,y2-y1



	# Corners
	# color
	_corners = []

	def _create_corners(self):
		self._corners = []
		t = Texture.from_file("assets/ui/cursor.png")
		s1 = MySprite(t); s1.clip.set(8,8); s1.clip.use(0,0)
		s2 = MySprite(t); s2.clip.set(8,8); s2.clip.use(2,0)
		s3 = MySprite(t); s3.clip.set(8,8); s3.clip.use(0,2)
		s4 = MySprite(t); s4.clip.set(8,8); s4.clip.use(2,2)
		s2.origin = -TILE+8,0
		s3.origin = 0,-TILE+8
		s4.origin = -TILE+8,-TILE+8
		self._corners = [[s1,s2],[s3,s4]]

	def _update_corners_position(self):
		self._corners[0][0].position = self.x1, self.y1
		self._corners[0][1].position = self.x2, self.y1
		self._corners[1][0].position = self.x1, self.y2
		self._corners[1][1].position = self.x2, self.y2

	def _update_corners_alpha(self):
		for side in self._corners:
			for edge in side:
				edge.color = self.color

	def _draw_corners(self, target, states):
		for side in self._corners:
			for edge in side:
				target.draw(edge, states)


