from sfml import Texture
from sfml import VertexArray, PrimitiveType, RenderStates
from sfml import Vertex

class Background:
# * Creates a vertex array.
	
	def __init__(self, window):
		self._make_vertex_array(*window.size)

	def draw(self, window, camera):
		window.view = window.default_view
		window.draw(self.vertex_array, self.render_states)
		window.view = camera

	#

	def _make_vertex_array(self, w,h):
		d = "assets/backgrounds/1.png"
		t = Texture.from_file(d)

		s = PrimitiveType.QUADS
		self.vertex_array = VertexArray(s)

		w,h = (w/t.width)+1,(h/t.height)+1
		for x in range(w):
			for y in range(h):

				v = Vertex; points = [v(),v(),v(),v()]
				x1, y1 = x*t.width, y*t.height
				x2, y2 = x1+t.width, y1+t.height

				#pos
				points[0].position = x1,y1
				points[1].position = x2,y1
				points[2].position = x2,y2
				points[3].position = x1,y2

				#tex
				x1, y1, x2, y2 = 0,0,t.width,t.height
				points[0].tex_coords = x1,y1
				points[1].tex_coords = x2,y1
				points[2].tex_coords = x2,y2
				points[3].tex_coords = x1,y2

				for point in points:
					self.vertex_array.append(point)

		self.render_states = RenderStates()
		self.render_states.texture = t