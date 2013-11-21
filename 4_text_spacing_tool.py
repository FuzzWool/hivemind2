from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Camera
from code.sfml_plus import Mouse

################################# 

from sfml import RectangleShape, Color
from sfml import Texture
from code.sfml_plus import MySprite
from code.sfml_plus import Rectangle

class Text_Spacing_Tool:
# A standalone tool. Not to be included with the game.
# WIP - Creates spaced text assets.

	def __init__(self, name):
		self._render_sprite(name)
		self._create_boxes()
		self.Select = self.Select()

	def controls(self, Camera, Mouse, Key):
		px = round(Mouse.x/Camera.zoom)
		py = round(Mouse.y/Camera.zoom)

		Box = self.box_upper[0]
		if Mouse.left.pressed():
			Box.x1, Box.y1 = px,py
		if Mouse.left.held():
			Box.x2, Box.y2 = px,py
		Box.render()

	def draw(self, window):
		self.Select.draw(window)
		for box in self.box_upper: window.draw(box())
		for box in self.box_lower: window.draw(box())
		for box in self.box_grammar: window.draw(box())
		window.draw(self.sprite)

	#

	def _render_sprite(self, name): #init
		d = "assets/fonts/%s.png" % name
		t = Texture.from_file(d)
		self.sprite = MySprite(t)



	characters = "abcdefghijklmnopqrstuvwxyz "
	grammar = ".:,;-!"
	def _create_boxes(self): #init
		self.box_upper = []
		self.box_lower = []
		self.box_grammar = []

		for character in self.characters:
			self.box_upper.append(self.Box())
			self.box_lower.append(self.Box())
		for character in self.grammar:
			self.box_grammar.append(self.Box())


	class Box(Rectangle):
	# The box which highlights a letter.

		def __init__(self): self.render()

		def render(self): #draw
			box = RectangleShape(self.size)
			box.position = self.position
			box.outline_thickness = 1
			box.outline_color = Color(255,0,0,100)
			box.fill_color = Color(0,0,0,10)
			self.box = box

		def __call__(self): return self.box



	class Select(Rectangle):
	# WIP - A tool which contains the selected rectangle.
	# WIP - Contains a box for highlighting the selected letter.

		def __init__(self):
			self._create_highlight()

		_selected = False
		def __call__(self, Box=None):
			if Box: self._selected = Box
			else: return self._selected 

		def draw(self, Window):
			Window.draw(self.highlight)

		#

		def _create_highlight(self): #init
			w,h = 8,12
			highlight = RectangleShape((w,h))
			highlight.position = self.position
			highlight.fill_color = Color(100,100,100,100)
			self.highlight = highlight


#################################

Window = Window((1200,600), "Text Spacing Tool")
Text_Spacing_Tool = Text_Spacing_Tool("speech")
Camera = Camera(Window)
Camera.zoom = 5
Camera.position = 0,0
Mouse = Mouse(Window)

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

		Text_Spacing_Tool.controls(Camera, Mouse, Key)

	Window.view = Camera
	Window.clear((255,255,255))
	Text_Spacing_Tool.draw(Window)
	Window.display(Mouse)