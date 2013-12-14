from code.sfml_plus import Rectangle
from sfml import RectangleShape
from sfml import Color
from code.sfml_plus.constants import TILE

class Grid(Rectangle):
#Provide the points: Create a grid around a rectangle.
# ! color and graphics are tweaked for UIBox.

	graphics = []	
	horizontal_lines = []
	vertical_lines = []

	def __init__(self, points):
		self.points = points

	def draw(self, Window):
		self._auto_make_lines()
		for line in self.vertical_lines:
			Window.draw(line)
		for line in self.horizontal_lines:
			Window.draw(line)


	######################################

	#COLOR
	#Forcefully dumbs down the alpha for UIBox.

	_color = Color(0,0,0,50)
	@property
	def color(self): return self._color
	@color.setter
	def color(self,color):
		color.a /= 5
		self._color = color
		self._make_lines()


	#LINES
	#

	old_points = 0,0,0,0
	def _auto_make_lines(self): #draw
		if self.old_points != self.points:
			self._make_lines()
		self.old_points = self.points

	def _make_lines(self): #auto
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