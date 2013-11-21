from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Camera
from code.sfml_plus import Mouse

################################# 

class Text_Ref:
	characters = "abcdefghijklmnopqrstuvwxyz "
	grammar = ".:,;-!"


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
		self.Select = self.Select(self.all_boxes)

	def controls(self, Camera, Mouse, Key, Window):
		px = round(Mouse.x/Camera.zoom)
		py = round(Mouse.y/Camera.zoom)

		self.Select.controls(Key, Window)
		Box = self.Select()
		# if Mouse.left.pressed():
		# 	Box.x1, Box.y1 = px,py
		# if Mouse.left.held():
		# 	Box.x2, Box.y2 = px,py
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

		for character in Text_Ref.characters:
			self.box_lower.append(self.Box(character))
			upper_char = character.upper()
			self.box_upper.append(self.Box(upper_char))
		for character in Text_Ref.grammar:
			self.box_grammar.append(self.Box(character))

		self.all_boxes =\
		[self.box_upper, self.box_lower, self.box_grammar]


	class Box(Rectangle):
	# The box which highlights a letter.

		def __init__(self, character):
			self.render()
			self.character = character #Select

		def render(self): #draw
			box = RectangleShape(self.size)
			box.position = self.position
			box.outline_thickness = 1
			box.outline_color = Color(255,0,0,100)
			box.fill_color = Color(0,0,0,10)
			self.box = box

		def __call__(self): return self.box



	class Select(Rectangle):
	# * A tool which contains the selected box.
	# Works out which box to select based on key input.
	# * Highlights the selected letter.

		def __init__(self, all_boxes):
			self.all_boxes = all_boxes
			self._selected = self.all_boxes[0][0]
			self._create_highlight()


		def controls(self, Key, Window):
			if not Window.key_pressed: return
			char = Window.key_pressed

			#grammar
			if Key.L_SHIFT.held():
				if char == "SEMI_COLON": char = ":"
				if char == "NUM1": char = "!"
			else:
				if char == "PERIOD": char = "."
				if char == "COMMA": char = ","
				if char == "SEMI_COLON": char = ";"
				if char == "DASH": char = "-"

			#caps
			if Key.L_SHIFT.held(): char = char.upper()
			else: char = char.lower()
			#

			y = 0
			for boxes in self.all_boxes:
				x = 0
				for box in boxes:
					if char == box.character:
						self(self.all_boxes[y][x])
						self._create_highlight()
					x += 1
				y += 1

		#
		def __call__(self, Box=None):
			if Box: self._selected = Box
			else: return self._selected 


		def draw(self, Window):
			Window.draw(self.highlight)

		#

		def _create_highlight(self): #init, controls
			
			#Find the position of the current box.
			char = self().character

			x, y = 0,0
			if char in Text_Ref.characters.upper():
				x =Text_Ref.characters.upper().index(char)
				y = 0
			if char in Text_Ref.characters:
				x = Text_Ref.characters.index(char)
				y = 1
			if char in Text_Ref.grammar:
				x = Text_Ref.grammar.index(char)
				y = 2

			#Highlight it
			w,h = 8,12
			highlight = RectangleShape((w,h))
			highlight.position = w*x, h*y
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

		Text_Spacing_Tool\
		.controls(Camera, Mouse, Key, Window)

	Window.view = Camera
	Window.clear((255,255,255))
	Text_Spacing_Tool.draw(Window)
	Window.display(Mouse)