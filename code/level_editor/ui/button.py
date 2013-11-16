from sfml import RectangleShape, Color
from sfml import Font, Text
from code.sfml_plus import Rectangle

class Button(Rectangle):
	
	held = False
	pressed = False
	was_held = False #

	def controls(self, events, Window, Key, Mouse):
		
		#STATES
		a, b = Mouse.position, self.points
		mouse_over = bool(Rectangle().in_points(a,b))

		self.held = False
		if Mouse.left.held() and mouse_over:
			self.held = True
		
		released = bool(self.was_held and not self.held)
		self.pressed = False
		if released and mouse_over:
			self.pressed = True
		self.was_held = self.held


		#EVENT
		if self.pressed: events["button_pressed"]= self.id


	def draw(self, Window, Camera):
		self._create_rectangle()
		self._create_text(self.string)
		Window.draw(self.rectangle)
		Window.draw(self.text)


	####

	def __init__(self, id):
		self.id = id
		self.size = 60, 30
		self._create_font()


	###
	#GRAPHICS

	rectangle = None
	def _create_rectangle(self): #draw
		rectangle = RectangleShape((10,10))

		rectangle.position = self.position
		rectangle.size = self.size

		rectangle.outline_color = Color.BLACK
		rectangle.outline_thickness = 1

		#events
		if self.held: rectangle.outline_thickness = 5
		if self.pressed: rectangle.outline_thickness = 10
		#

		self.rectangle = rectangle

	#

	font = None
	def _create_font(self): #init
		d = "assets/fonts/PIXEARG_.ttf"
		font = Font.from_file(d)
		self.font = font
		self.font.get_texture(8).smooth = False

	text = None
	string = "OKAY"
	padding = 2
	def _create_text(self, string=""): #init, input
		text = Text(string)
		text.font = self.font
		text.character_size = 8
		text.style = Text.REGULAR
		text.color = Color.BLACK

		x = self.center[0]-(text.global_bounds.width/2)
		y = self.center[1]-(text.global_bounds.height/2)
		text.position= x,y

		self.text = text
		self.string = string