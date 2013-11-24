from sfml import Texture
from sfml import Drawable
from sfml import Vertex, VertexArray
from sfml import PrimitiveType, RenderStates
from code.sfml_plus.graphics import Rectangle

from sfml import Color


class _Loader:
# * Loads the texture.
# * Load the boundary data.

	def __init__(self, name):
		d = "assets/fonts/%s" % name
		self._load_texture(d)
		self._load_boundaries(d)


	characters = "abcdefghijklmnopqrstuvwxyz "
	grammar = ".:,;-!"
	def get_character_points(self, character):
		x, y = 0,0
		c = character
		if c in self.characters:
			x = self.characters.index(c)
			y = 1
		elif c in self.characters.upper():
			x = self.characters.upper().index(c)
			y = 0
		elif c in self.grammar:
			x = self.grammar.index(c)
			y = 2

		x1,y1,x2,y2 = self.boundaries[y][x]
		x1 -= 1; y1 -= 1
		x2 += 1; y2 += 1
		#
		y1 = 12*y; y2 = 12*(y+1)
		#
		return x1,y1,x2,y2

	#

	texture = None
	def _load_texture(self, directory): #init
		self.texture = Texture.from_file(directory+".png")

	boundaries = None
	def _load_boundaries(self, directory): #init

		#open
		f = open(directory+".txt","r")
		load_data = f.read()
		f.close()

		#format
		load_data = load_data.split("\n")
		new_load_data = []
		for line in load_data:
			line = line.translate(None, "(")
			line = line.split(")")
			
			new_line = []
			for values in line:
				values = values.split(", ")
				
				if values[0] != "":
					new_values = []
					for value in values:
						new_values.append(float(value))

					new_line.append(new_values)

			new_load_data.append(new_line)
		load_data = new_load_data

		self.boundaries = load_data

Loader = _Loader("speech")



class _Text:

	letters = []
	def _create_letters(self): #write, x/y
		letters = []

		total_w, total_h = self.x, self.y
		for character in self.string:

			if character == "\n":
				total_w = self.x
				total_h += 12
			else:
				pos = total_w, total_h
				Letter = self.Letter(pos, character)
				letters.append(Letter)

				p = Loader.get_character_points(character)
				w = p[2]-p[0]
				
				total_w += w+1

		self.letters = letters


	def _create_vertex_array(self): #draw
		letters = self.letters

		s = PrimitiveType.QUADS
		vertex_array = VertexArray(s)
		
		#

		for Letter in letters:
			Letter.create_vertex()
			for vertice in Letter.vertex:
				vertex_array.append(vertice)

		#

		self.vertex_array = vertex_array
		self.render_states = RenderStates()
		t = Texture.from_file("assets/fonts/speech.png")
		self.render_states.texture = Loader.texture


class _Letter:
# * Creates a vertex upon being initialized.

	characters = "abcdefghijklmnopqrstuvwxyz "
	grammar = ".:,;-!"

	def create_vertex(self): #Text.create_vertex_array
		vertex = []
		for i in range(4): vertex.append(Vertex())

		color = self.color
		l = self.letter
		
		#position
		p = Loader.get_character_points(l)
		w,h = p[2]-p[0], p[3]-p[1]
		x1,y1 = self.position
		x2,y2 = x1+w, y1+h

		vertex[0].position = x1,y1
		vertex[1].position = x2,y1
		vertex[2].position = x2,y2
		vertex[3].position = x1,y2

		#clipping
		x1,y1,x2,y2 = Loader.get_character_points(l)
		vertex[0].tex_coords = x1, y1
		vertex[1].tex_coords = x2, y1
		vertex[2].tex_coords = x2, y2
		vertex[3].tex_coords = x1, y2

		#color
		for vertice in vertex: vertice.color = color

		self.w, self.h = w,h
		self.vertex = vertex



class Text(_Text, Drawable, Rectangle):
# * batches Letters
# * Position
# * Color

	def __init__(self, *args): self.write(*args)


	#LOOP
	def draw(self, target, states):
		self._create_vertex_array()
		target.draw(self.vertex_array, self.render_states)
	#


	#CALL
	string = ""
	def write(self, string):
		self.string = string
		self._create_letters()
		self._create_vertex_array()

	#POSITION
	_x, _y = 0,0

	@property
	def x(self): return self._x
	@x.setter
	def x(self, x):
		amt = x - self._x
		self._x = x
		for letter in self.letters:
			letter.x += amt

	@property
	def y(self): return self._y
	@y.setter
	def y(self, y):
		amt = y - self._y
		self._y = y
		for letter in self.letters:
			letter.y += amt

	@property
	def w(self):
		return self.letters[-1].x2 - self.letters[0].x1

	@property
	def h(self):
		return self.letters[-1].y2 - self.letters[0].y1
	#

	#COLOR
	_color = Color(255,255,255,255)
	@property
	def color(self): return self._color
	@color.setter
	def color(self, Color):
		for letter in self.letters:
			letter.color = Color
		self._color = Color
	#


	class Letter(_Letter, Rectangle):
	# * Position
	# * Color

		def __init__(self, position, letter):
			self.position = position
			self.size = 0,0
			self.letter = letter

		#

		color = Color(255,255,255,255)