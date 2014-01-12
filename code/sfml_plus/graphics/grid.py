from sfml import Drawable, RectangleShape, Color
from code.sfml_plus.graphics import Rectangle
from code.sfml_plus.constants import TILE

#Grid_Room
from sfml import Drawable
from code.sfml_plus.graphics import Rectangle

#_Rendered_Grid_Room
from sfml import Drawable, RectangleShape, Color
from sfml import RenderTexture, Sprite
from code.sfml_plus.graphics import Rectangle
from code.sfml_plus.constants import TILE
from code.sfml_plus.constants import ROOM_WIDTH, ROOM_HEIGHT


#Grid
#Grid_Room

class Grid(Drawable, Rectangle):
	
	#################################
	# PUBLIC

	def __init__(self, w,h):
		Drawable.__init__(self)
		self.color = Color.BLACK
		self.w, self.h = w,h

	def draw(self, target, states):
		self._create_Lines()
		self._draw_Lines(target, states)

	#

	color = Color.BLACK

	#################################
	# PRIVATE

	# Lines
	_rows = []
	_columns = []

	def _create_Lines(self):
		
		self._columns = []
		for x in range(self.tile_w+1):
			r = RectangleShape((1,self.h))
			r.fill_color = self.color
			r.position = self.x+(TILE*x), self.y
			self._columns.append(r)

		self._rows = []
		for y in range(self.tile_h+1):
			r = RectangleShape((self.w,1))
			r.fill_color = self.color
			r.position = self.x, self.y+(TILE*y)
			self._rows.append(r)


	def _draw_Lines(self, target, states):
		for line in self._columns+self._rows:
			target.draw(line, states)


################################################

class _Rendered_Grid_Room(Drawable, Rectangle):
# Drawable, forwards to Sprite
# * Generated and rendered ONCE globally when called.
	
	#################################
	# PUBLIC

	sprite = None

	def __init__(self):
		Drawable.__init__(self)
		self.w, self.h = ROOM_WIDTH, ROOM_HEIGHT
		self._create_Lines()
		self._render_Lines()

	def draw(self, target, states):
		self._draw_Lines(target, states)

	#

	color = Color(255,255,255,255)

	#################################
	# PRIVATE

	# Lines
	_rows = []
	_columns = []

	def _create_Lines(self): #init
		
		self._columns = []
		for x in range(self.tile_w+1):
			w = 1
			if x == 0 or x == self.tile_w: w = 5
			r = RectangleShape((w,self.h))
			r.fill_color = self.color
			r.position = self.x+(TILE*x)-(w/2), self.y
			self._columns.append(r)

		self._rows = []
		for y in range(self.tile_h+1):
			h = 1
			if y == 0 or y == self.tile_h: h = 5
			r = RectangleShape((self.w,h))
			r.fill_color = self.color
			r.position = self.x, self.y+(TILE*y)-(h/2)
			self._rows.append(r)

	# Rendering
	_texture = RenderTexture(ROOM_WIDTH+1, ROOM_HEIGHT+1)

	def _render_Lines(self): #init
		for line in self._columns+self._rows:
			self._texture.draw(line)
		self._texture.display()
		self.sprite = Sprite(self._texture.texture)

	def _draw_Lines(self, target, states): #draw
		target.draw(self.sprite, states)



class Grid_Room(Drawable, Rectangle):
# Drawable
# * Uses a pre-rendered sprite. Size cannot be changed.
# (Sprite is rendered ONCE as a global upon access.)

	#################################
	# PUBLIC

	def draw(self, target, states):
		self._Grid_Room.sprite.position = self.position
		target.draw(self._Grid_Room, states)

	#################################
	# PRIVATE

	_Grid_Room = _Rendered_Grid_Room()
	_Grid_Room.sprite.color = Color(0,0,0,100)


################################################