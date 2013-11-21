from code.sfml_plus import Window
from code.sfml_plus import Key

#################################

from sfml import Drawable
from sfml import Vertex, VertexArray
from sfml import PrimitiveType, RenderStates
from sfml import Texture
from code.sfml_plus import Rectangle

class Text(Drawable):
#A text class which follows the sfml_plus standard.
# * loads Text characters from image files.

	def __init__(self):
		Drawable.__init__(self)

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

		x,y = 0,0
		w,h = 8,12
		for character in self.string:


			if character == "\n":
				x = 0
				y += 1
			else:
				points = (x*w, y*h, (x+1)*w, (y+1)*h)
				Letter = self.Letter(points, character)
				letters.append(Letter)
				x += 1

		self.letters = letters

	def _create_vertex_array(self): #write
		s = PrimitiveType.QUADS
		vertex_array = VertexArray(s)
		
		#

		for Letter in self.letters:
			Letter.create_vertex()
			for vertice in Letter.vertex:
				vertex_array.append(vertice)

		#

		self.vertex_array = vertex_array
		self.render_states = RenderStates()
		t = Texture.from_file("assets/fonts/speech.png")
		self.render_states.texture = t



	class Letter(Rectangle):
	# * positioning.
	# * clipping.

		def __init__(self, points, letter):
			self.points = points
			self.letter = letter


		characters = "abcdefghijklmnopqrstuvwxyz "
		grammar = ".:,;-!"

		def create_vertex(self):
			vertex = []
			for i in range(4): vertex.append(Vertex())

			#position
			vertex[0].position = self.x1, self.y1
			vertex[1].position = self.x2, self.y1
			vertex[2].position = self.x2, self.y2
			vertex[3].position = self.x1, self.y2

			#clipping
			x, y = 26,0
			l = self.letter

			if l in self.characters:
				x = self.characters.index(l)
				y = 1
			elif l in self.characters.upper():
				x = self.characters.upper().index(l)
				y = 0
			elif l in self.grammar:
				x = self.grammar.index(l)
				y = 2

			x1, y1 = self.w*x, self.h*y
			x2, y2 = x1+self.w, y1+self.h
			vertex[0].tex_coords = x1, y1
			vertex[1].tex_coords = x2, y1
			vertex[2].tex_coords = x2, y2
			vertex[3].tex_coords = x1, y2

			self.vertex = vertex


#################################

Window = Window((1200,600), "Text Class")

Text = Text()
Text.write("Hello there, my name is Sam.\nThis is a test!")

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((255,255,255))
	Window.draw(Text)
	Window.display()