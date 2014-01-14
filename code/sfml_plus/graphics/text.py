from sfml import Texture
from sfml import Drawable
from sfml import Vertex, VertexArray
from sfml import PrimitiveType, RenderStates
from code.sfml_plus.graphics import Rectangle

from sfml import Color

class Ref:
	characters = "abcdefghijklmnopqrstuvwxyz "
	grammar = ".:,;-!()'*/?"
	numbers = "0123456789"


class Font:
# * Loads the texture.
# * Load the boundary data.

	def __init__(self, name):
		d = "assets/fonts/%s" % name
		self._load_texture(d)
		self._load_boundaries(d)
		self.characters = Ref.characters
		self.grammar = Ref.grammar
		self.numbers = Ref.numbers

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
		elif c in self.numbers:
			x = self.numbers.index(c)
			y = 3

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


class _Text:

	letters = []
	def _create_letters(self): #write, x/y
		Font = self.Font
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

				p = Font.get_character_points(character)
				w = p[2]-p[0]
				
				total_w += w+1

		self.letters = letters


	def _create_vertex_array(self): #draw
		Font = self.Font
		letters = self.letters

		s = PrimitiveType.QUADS
		vertex_array = VertexArray(s)
		
		#

		for Letter in letters:
			Letter.create_vertex(Font)
			for vertice in Letter.vertex:
				vertex_array.append(vertice)

		#

		self.vertex_array = vertex_array
		self.render_states = RenderStates()
		t = Texture.from_file("assets/fonts/speech.png")
		self.render_states.texture = Font.texture


class _Letter:
# * Creates a vertex upon being initialized.

	def __init__(self):
		self.characters = Ref.characters
		self.grammar = Ref.grammar
		self.numbers = Ref.numbers

	def create_vertex(self, Font): #Text...vertex_array
		vertex = []
		for i in range(4): vertex.append(Vertex())

		color = self.color
		l = self.letter
		
		#position
		p = Font.get_character_points(l)
		w,h = p[2]-p[0], p[3]-p[1]
		x1,y1 = self.position
		x2,y2 = x1+w, y1+h

		vertex[0].position = x1,y1
		vertex[1].position = x2,y1
		vertex[2].position = x2,y2
		vertex[3].position = x1,y2

		#clipping
		x1,y1,x2,y2 = Font.get_character_points(l)
		vertex[0].tex_coords = x1, y1
		vertex[1].tex_coords = x2, y1
		vertex[2].tex_coords = x2, y2
		vertex[3].tex_coords = x1, y2

		#color
		for vertice in vertex: vertice.color = color

		self.w, self.h = w,h
		self.vertex = vertex



class Text(_Text, Drawable, Rectangle):
# * loads a Font
# * batches Letters
# * Position
# * Color

	def __init__(self, Font):
		self.Font = Font


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
		try:
			return self.letters[-1].x2-self.letters[0].x1
		except: return 0

	@property
	def h(self):
		try: return self.letters[-1].y2-self.letters[0].y1
		except: return 0
	#

	#COLOR
	_color = Color(255,255,255,255)
	@property
	def color(self): return self._color
	@color.setter
	def color(self, c):
		color = [v for v in c]
		for letter in self.letters:
			letter.color = Color(*color)
		self._color = Color(*color)
	#


	class Letter(_Letter, Rectangle):
	# * Position
	# * Color

		def __init__(self, position, letter):
			self.position = position
			self.size = 0,0
			self.letter = letter
			self.color = Color(255,255,255,255)



################################




class Multiline_Text(Drawable, Rectangle):

	#################################
	# PUBLIC

	###
	#Core

	x,y,w,h = 0,0,0,0
	Font = None
	padding = 10

	def __init__(self, Font):
		self.Font = Font

	def draw(self, target, states):
		self._draw_Text_rows(target, states)

	###
	# Writing Styles

	def write(self, text):
		self._create_Text_rows(text)

	def say(self, text):
		pass


	#################################
	# PRIVATE

	###
	# Text Rows

	_Text_rows = []

	def _create_Text_rows(self, t): #write

		def new_row(text):
			#Create a Text row.
			new_row = Text(self.Font)
			new_row.write(text)
			new_row.position = self.x+self.padding, self.y+self.padding
			return new_row

		def new_index(text):
			#Find all the spaces in the string (word indexing).
			def find(string, wanted_char):
				for i, char in enumerate(string):
					if char == wanted_char:
						yield i
			return list(find(text, " "))


		def add_rows(text):
			#Create a new row each time the last exceeds the width.
			row = new_row(text)
			index = new_index(text)
			old_i = 0
			broken = False

			for i in index:
				w = row.letters[i].x2 - row.letters[0].x1
				w += row.letters[i].x2 - row.letters[old_i].x1
				max_w = self.w
				if w > max_w:
					row.write(text[:old_i])
					self._Text_rows.append(row)
					add_rows(text[old_i+1:])
					broken = True; break
				old_i = i

			if not broken:
				row.write(text)
				self._Text_rows.append(row)


		self._Text_rows = []
		# add_rows(t)
		sentences = t.split("\n")
		for line in sentences:
			add_rows(line)

		#adjust height
		for i, row in enumerate(self._Text_rows):
			row.y += i*row.h


	def _draw_Text_rows(self, target, states): #draw
		for row in self._Text_rows:
			target.draw(row, states)
