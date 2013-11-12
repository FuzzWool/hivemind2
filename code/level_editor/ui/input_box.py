from sfml import Text, Font
from sfml import Color
from sfml import KeyEvent

from sfml import VertexArray, PrimitiveType
from sfml import Clock

from sfml import RectangleShape
from code.sfml_plus import Rectangle

class InputBox(Rectangle):
# * May have text inputted with a keyboard.
# * Box has a flickering cursor.

	string = ""

	def __init__(self):
		self._create_font()
		self._create_text()
		self.cursor = self.cursor()

	def controls(self, window, key):
		self._input(window, key)

	def draw(self, window, camera):
		self._create_rectangle()
		window.draw(self.rectangle)

		window.draw(self.text)

		self.cursor.create(self.text)
		window.draw(self.cursor.line)


	#####
	# RECTANGLE

	padding = 2
	@property
	def x(self): return self.text.position[0]-self.padding
	@property
	def y(self): return self.text.position[1]-self.padding
	@property
	def w(self): return 100 + self.padding
	@property
	def h(self):
		return self.text.character_size + (self.padding*2)

	@x.setter
	def x(self, x):
		self.text.position \
		= x+self.padding, self.text.position[1]
	@y.setter
	def y(self, y):
		self.text.position \
		= self.text.position[0], y+self.padding


	###
	#GRAPHICS

	font_size = 8

	#

	font = None
	def _create_font(self): #init
		d = "assets/fonts/PIXEARG_.ttf"
		font = Font.from_file(d)
		self.font = font
		self.font.get_texture(8).smooth = False

	text = None
	string = None
	def _create_text(self, string=""): #init, input
		text = Text(string)
		text.font = self.font
		text.character_size = 8
		text.style = Text.REGULAR
		text.color = Color.BLACK
		try:
			x = self.position[0]+self.padding
			y = self.position[1]+self.padding
			text.position = x,y
		except: text.position = 0,0
		self.text = text
		self.string = string


	#

	class cursor:
	#A cursor aligned to text.

		def __init__(self):
			line = None
			self.clock = Clock()
			self.flicker = False

		def create(self, text): #draw
			line = VertexArray(PrimitiveType.LINES, 2)

			self._flicker()
			if self.flicker:
				x, y, w, h = text.global_bounds

				line[0].position = (x+w,y)
				line[1].position = (x+w,y+h)

				line[0].color = Color.BLACK
				line[1].color = Color.BLACK
			self.line = line

		def _flicker(self): #create
			if self.clock.elapsed_time.seconds > 0.5:
				self.flicker = not self.flicker
				self.clock.restart()


	rectangle = None
	def _create_rectangle(self): #draw
		rectangle = RectangleShape((10,10))

		rectangle.position = self.position
		rectangle.size = self.size

		rectangle.outline_color = Color.BLACK
		rectangle.outline_thickness = 1

		self.rectangle = rectangle

	###

	def _input(self, window, key): #controls
		def add_chr(key_chr):
			self.string += key_chr
			self._create_text(self.string)

		def remove_chr():
			if len(self.string) >= 1:
				self.string = self.string[:-1]
				self._create_text(self.string)

		if window.key_pressed:
			key_chr = str(window.key_pressed)

			if key_chr.isalpha() and len(key_chr) == 1:
				if key.L_SHIFT.held():
					add_chr(key_chr.upper())
				else:
					add_chr(key_chr.lower())

				#Can't exceed box length.
				w = self.text.global_bounds.width
				if w+2 > self.w:
					remove_chr()
				#

			if key_chr == "BACKSPACE":
				remove_chr()
			if key_chr == "SPACE":
				add_chr(" ")