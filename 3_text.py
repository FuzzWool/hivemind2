from code.sfml_plus import Window
from code.sfml_plus import Key

#################################

from sfml import Texture

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



from sfml import Drawable
from sfml import Vertex, VertexArray
from sfml import PrimitiveType, RenderStates
from code.sfml_plus import Rectangle

class Text(Drawable):
#A text class which follows the sfml_plus standard.
# * loads Text characters from image files.

	def __init__(self):
		Drawable.__init__(self)
		self.Loader = _Loader("speech")

	def draw(self, target, states):
		target.draw(self.vertex_array, self.render_states)


	string = ""
	def write(self, string):
		self.string = string
		self._create_letters()
		self._create_vertex_array()

	#

	def _create_letters(self): #write
		letters = []

		total_w, total_h = 0, 0
		for character in self.string:


			if character == "\n":
				total_w = 0
				total_h += 12
			else:
				x1, y1 = total_w, total_h
				Letter = self.Letter((x1,y1),character)
				letters.append(Letter)

				_p = self.Loader\
				.get_character_points(character)
				w = _p[2]-_p[0]
				
				total_w += w+1

		self.letters = letters


	def _create_vertex_array(self): #write
		letters = self.letters

		s = PrimitiveType.QUADS
		vertex_array = VertexArray(s)
		
		#

		for Letter in letters:
			Letter.create_vertex(self.Loader)
			for vertice in Letter.vertex:
				vertex_array.append(vertice)

		#

		self.vertex_array = vertex_array
		self.render_states = RenderStates()
		t = Texture.from_file("assets/fonts/speech.png")
		self.render_states.texture = self.Loader.texture



	class Letter(Rectangle):
	# * positioning.
	# * clipping.

		def __init__(self, position, letter):
			self.position = position
			self.letter = letter


		characters = "abcdefghijklmnopqrstuvwxyz "
		grammar = ".:,;-!"

		def create_vertex(self, Loader):
			vertex = []
			for i in range(4): vertex.append(Vertex())

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

			self.vertex = vertex


#################################

Window = Window((1200,600), "Text Class")

Text = Text()
# Text.write("Hello there, my name is Sam.\nTesting!")
# Text.write("THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG.")
Text.write("The quick brown fox jumped over the lazy dog.")

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((255,255,255))
	Window.draw(Text)
	Window.display()