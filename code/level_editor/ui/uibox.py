from code.sfml_plus import Rectangle
from sfml import RectangleShape
from sfml import Color


class UIBox(Rectangle):
# * Positions UI objects within itself.

	w,h = 300,100

	def controls(self, window, key, mouse):
		for ui in self.contents:
			ui.controls(window, key, mouse)

	def draw(self, window, camera):
		self._create_rect()
		window.draw(self.rectangle)
		for ui in self.contents:
			ui.draw(window, camera)


	# RECTANGLE

	rectangle = None
	def _create_rect(self): #draw
		rectangle = RectangleShape(self.size)
		rectangle.position = self.position

		rectangle.fill_color = Color(255,150,100)
		rectangle.outline_color = Color.BLACK
		rectangle.outline_thickness = 1
		
		self.rectangle = rectangle


	# CONTENTS

	contents = []
	def add(self, ui, pos):
		ui = ui()
		ui.position = self.x+pos[0], self.y+pos[1]
		self.contents.append(ui)

	# position

	_x, _y = 0,0
	@property
	def x(self): return self._x
	@property
	def y(self): return self._y

	@x.setter
	def x(self, x):
		dist = self._x - x
		self._x = x
		for ui in self.contents: ui.x -= dist

	@y.setter
	def y(self, y):
		dist = self._y - y
		self._y = y
		for ui in self.contents: ui.y -= dist