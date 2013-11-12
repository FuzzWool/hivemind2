from code.sfml_plus import Window
from code.sfml_plus import key

###################################

from code.sfml_plus import Rectangle
from sfml import RectangleShape
from sfml import Color


class ui_box(Rectangle):
# * Positions UI objects within itself.

	w,h = 300,100

	def controls(self, window, key):
		for ui in self.contents:
			ui.controls(window, key)

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


###################################

from code.level_editor.ui import InputBox
ui_box = ui_box()
ui_box.position = 100,100
ui_box.add(InputBox, (10,10))
ui_box.add(InputBox, (10,25))

###################################


window = Window((1200,600), "UI Box")
from code.sfml_plus import Camera
Camera = Camera(window)

while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed():
			ui_box.x += 100
		ui_box.controls(window, key)

	window.clear((255,255,255))
	ui_box.draw(window, Camera)
	window.display()