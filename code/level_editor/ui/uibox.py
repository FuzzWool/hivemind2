from code.sfml_plus import Rectangle
from sfml import RectangleShape
from sfml import Color


class UIBox(Rectangle):
# * Positions and processes UI objects within itself.
# * Handles outer events,
# 	ID'd based on which UI invokes them.

	contents = []
	def add(self, ui, pos):

		x, y = 0,0
		if pos[0] >= 0: x = self.x1 + pos[0]
		if pos[0] <  0: x = self.x2 + pos[0]
		if pos[1] >= 0: y = self.y1 + pos[1]
		if pos[1] <  0: y = self.y2 + pos[1]

		id = len(self.contents)
		ui = ui(id)
		
		if pos[0] < 0: x -= ui.w
		if pos[1] < 0: y -= ui.h
		ui.position = x,y
		
		self.contents.append(ui)


	#LOGIC
	events = {"button_pressed":None}

	def controls(self, Window, Key, Mouse):
		
		#Wipe the EVENTS.
		for key in self.events:
			self.events[key] = None

		#Handle any independant controls.
		#Process the EVENTS.
		for ui in self.contents:
			ui.controls(self.events, Window, Key, Mouse)


	# GRAPHICS
	w,h = 300,100

	def draw(self, window, camera):
		self._create_rect()
		window.draw(self.rectangle)
		for ui in self.contents:
			ui.draw(window, camera)


	####################################

	# RECTANGLE

	rectangle = None
	def _create_rect(self): #draw
		rectangle = RectangleShape(self.size)
		rectangle.position = self.position

		rectangle.fill_color = Color(255,150,100)
		rectangle.outline_color = Color.BLACK
		rectangle.outline_thickness = 1
		
		self.rectangle = rectangle


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