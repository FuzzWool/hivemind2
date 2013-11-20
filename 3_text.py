from code.sfml_plus import Window
from code.sfml_plus import Key

#################################

from sfml import Drawable
from sfml import Vertex, VertexArray
from sfml import PrimitiveType, RenderStates
from sfml import Texture

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
		self._create_vertex_array()

	#

	def _create_vertex_array(self): #write
		s = PrimitiveType.QUADS
		vertex_array = VertexArray(s)
		
		string = self.string
		characters = "abcdefghijklmnopqrstuvwxyz "
		grammar = ".:,;-!"

		### POINT
		w, h = 8,12
		x, y = 0,0
		for c in string:

			if c == "\n":
				x = 0
				y += 1

			else:

				points = self.points()

				w, h = 8,12
				x1, y1, x2, y2 = w*x,h*y,w*(x+1),h*(y+1)
				points.points(x1,y1,x2,y2)

				if c in characters:
					xc = characters.index(c)
					points.clip(xc,1)
				elif c in characters.upper():
					xc = characters.upper().index(c)
					points.clip(xc,0)
				elif c in grammar:
					xc = grammar.index(c)
					points.clip(xc,2)

				for point in points():
					vertex_array.append(point)
			
				x += 1
		#

		self.vertex_array = vertex_array
		self.render_states = RenderStates()
		t = Texture.from_file("assets/fonts/speech.png")
		self.render_states.texture = t


	class points:
	#WIP - Easy positioning/clipping for vertices.
		
		def __init__(self):
			self._p = []
			for i in range(4): self._p.append(Vertex())

		def points(self, x1, y1, x2, y2):
			self._p[0].position = x1,y1
			self._p[1].position = x2,y1
			self._p[2].position = x2,y2
			self._p[3].position = x1,y2
			self.w, self.h = x2-x1, y2-y1

		def clip(self, x, y):
			x1, y1 = x*self.w, y*self.h
			x2, y2 = x1+self.w, y1+self.h
			self._p[0].tex_coords = x1,y1
			self._p[1].tex_coords = x2,y1
			self._p[2].tex_coords = x2,y2
			self._p[3].tex_coords = x1,y2

		def __call__(self): return self._p


#################################

Window = Window((1200,600), "Text Class")

Text = Text()
Text.write("Hello there, my name is Sam.\nAha - Ahahaha!")

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((255,255,255))
	Window.draw(Text)
	Window.display()