from code.sfml_plus import Window
from code.sfml_plus import key

########################
# Sprites

from sfml import VertexArray, PrimitiveType, RenderStates
from sfml import Texture
from sfml import Vertex
from sfml import Color

s = PrimitiveType.QUADS
vertex_array = VertexArray(s)

def make_vertices():
	vertices = []

	#points
	point1 = Vertex()
	point2 = Vertex()
	point3 = Vertex()
	point4 = Vertex()
	points = [point1,point2,point3,point4]

	#position
	x1, y1, x2, y2 = 25,25,50,50
	point1.position = x1,y1
	point2.position = x2,y1
	point3.position = x2,y2
	point4.position = x1,y2
	print x1, y1, x2, y2

	#clip
	data = "0000"
	if not data == "____":
		clip_x = int(data[0:2])
		clip_y = int(data[2:4])

		TILE = 25
		x1 = (clip_x+0)*TILE
		y1 = (clip_y+0)*TILE
		x2 = (clip_x+1)*TILE
		y2 = (clip_y+1)*TILE
		print x1, y1, x2, y2

		point1.tex_coords = x1,y1
		point2.tex_coords = x2,y1
		point3.tex_coords = x2,y2
		point4.tex_coords = x1,y2

	else:
		for point in points:
			point.tex_coords = 0,0
			point.color = Color(0,0,0,0)

	for point in points:
		vertices.append(point)

	return vertices

vertices = make_vertices()
for point in vertices:
	vertex_array.append(point)

t = Texture.from_file("assets/tilesets/1.png")
render_states = RenderStates()
render_states.texture = t


########################

window = Window((600,300), "Hivemind - Demo 2")

while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed(): print 1

	window.clear((255,220,0))
	window.draw(vertex_array, render_states)
	window.display()