from code.sfml_plus.ui import _UI, Button
from sfml import RectangleShape, Color

class Slider(_UI): #horizontal
# Graphics
# * A variable amount of lines spanning the width.

	w,h = 150,15
	lines = 5
	value = float(0) # to 100

	def __init__(self):
		_UI.__init__(self)
		self._create_Box()

	def controls(self, Key, Mouse, Camera):
		_UI.controls(self, Key, Mouse, Camera)
		self._Box_controls(Mouse)

	def draw(self, Window):
		self._create_baseLine()
		self._create_Lines()
		lines = self.Lines + [self.baseLine]
		for line in lines: Window.draw(line)
		#
		self._parent_Box()
		self.Box.draw(Window)
		#
		_UI.draw(self, Window)

	####################

	### GRAPHICS
	# Creates measurement lines and a box.
	# create, pos/alpha, draw
	baseLine = None
	Lines = []
	Box = None

	def _create_baseLine(self):
		self.baseLine = RectangleShape((self.w,0))
		self.baseLine.position = self.x, self.center[1]
		self.baseLine.outline_thickness = 1
		self.baseLine.outline_color = Color(0,0,0)

		#color
		b = self.baseLine
		c=b.outline_color;c.a=self.alpha;b.outline_color=c


	def _create_Lines(self):
		self.Lines = []

		for i in range(self.lines):
			w = float(self.w)/(self.lines-1)

			line = RectangleShape((0,self.h))
			x = self.x+(w*(i))
			line.position = x, self.y
			line.outline_thickness = 1
			line.outline_color = Color.BLACK

			#color
			c=line.outline_color;c.a=self.alpha
			line.outline_color=c

			self.Lines.append(line)

	def _create_Box(self):
		self.Box = Button()
		self.Box.text = " "
		self.Box.size = 20,self.h
		self.Box.x -= (self.Box.w/2)
		self.Box.y -= self.Box.rise

	def _parent_Box(self):

		#Follow parents' movement/alpha.
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		if x_move: self.Box.x += x_move
		if y_move: self.Box.y += y_move
		#
		self.Box.alpha = self.alpha

	### LOGIC
	
	def _Box_controls(self, Mouse):
		self.Box.controls(None, Mouse, None)
		#
		
		#Hold and drag: move the cursor.
		if self.Box.held:
			v = Mouse.x - self.x1
			if v < 0: v = 0
			if v > self.w: v = self.w

			self.Box.x += (self.x1-self.Box.center[0])+v
			self.value = (float(v)/self.w)*100

		#Unpressed: go to nearest line.
		elif self.Box.selected:
			if self.lines > 2:
				w_chunk = float(self.w)/(self.lines-1)
				x = self.x
				midpoint = (w_chunk/2)-(self.Box.w/2)
				while x + midpoint < self.Box.x:
					x += w_chunk
				self.Box.tween.x = x-(self.Box.w/2)