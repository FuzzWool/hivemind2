from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

##########################################

from code.sfml_plus.ui import Box
from code.sfml_plus import Texture, MySprite
from code.sfml_plus import Rectangle
from code.sfml_plus import Grid
from code.sfml_plus.constants import TILE

from sfml import Color

class TileSelector(Box):
	
	#################################
	# PUBLIC

	def __init__(self):
		Box.__init__(self)
		self.Sheet = self.Sheet("0.png")
		self.size = self.Sheet.size
		self.Grid = Grid(*self.size)
		self.Cursor = self.Cursor()

	def controls(self, Key, Mouse, Camera):
		self.Cursor.controls(Key, Mouse, Camera)

	def draw(self, target, states):
		self._parent_Graphics()
		Box.draw(self, target, states)
		self.Sheet.draw(target, states)
		target.draw(self.Grid)
		self.Cursor.draw(target, states)

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
		c=self.Cursor.color;c.a=self.alpha;self.Cursor.color=c
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		self.Cursor.x += x_move
		self.Cursor.y += y_move


	# SHEET
	class Sheet(Rectangle):

		def __init__(self, name):
			Rectangle.__init__(self)
			self._create_sprite(name)

		def draw(self, target, states):
			self._parent_sprite()
			self._draw_sprite(target, states)
		#

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



	#CURSOR
	class Cursor(Rectangle):
		
		#################################
		# PUBLIC

		snap = True
		color = Color.WHITE

		def __init__(self):
			self._create_corners()
			self.snap = True
			self.color = Color.WHITE

		def controls(self, Key, Mouse, Camera):
			self._update_position(Mouse)

		def draw(self, target, states):
			self._update_corners_position()
			self._update_corners_alpha()
			self._draw_corners(target, states)

		#################################
		# PRIVATE

		# Position
		# snap
		def _update_position(self, Mouse):
			if self.snap:
				self.tile_position = Mouse.tile_position

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
			self._corners[0][1].position = self.x1, self.y2
			self._corners[1][0].position = self.x2, self.y1
			self._corners[1][1].position = self.x2, self.y2

		def _update_corners_alpha(self):
			for side in self._corners:
				for edge in side:
					edge.color = self.color

		def _draw_corners(self, target, states):
			for side in self._corners:
				for edge in side:
					target.draw(edge, states)



##########################################


from code.sfml_plus.ui import Box
from code.sfml_plus.ui import Accept_Button, Cancel_Button

Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()
box1.w += 250; box1.h += 100
box1.center = Window.center

box2 = Accept_Button()
box2.x += box1.w - box2.w
box2.y += (box1.h - box2.h) - box2.rise
box1.children.append(box2)

tileselector = TileSelector()
tileselector.tile_x += 1; tileselector.tile_y += 1
box1.children.append(tileselector)

##########################################

while Window.is_open:
	if Window.is_focused:

		if box2.selected\
		or Key.BACKSPACE.pressed():
			box1.close()

		if Key.ENTER.pressed():
			box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display(Mouse)