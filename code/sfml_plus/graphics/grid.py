from sfml import Drawable, RectangleShape, Color
from code.sfml_plus.graphics import Rectangle
from code.sfml_plus.constants import TILE

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
