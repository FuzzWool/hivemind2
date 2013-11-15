from code.sfml_plus import Window
from code.sfml_plus import Key

###################################
from sfml import RectangleShape, Color
from sfml import Font, Text
from code.sfml_plus import Rectangle

class Button(Rectangle):
	
	def controls(self, Window, Key, Mouse):
		pass

	def draw(self, Window, Camera):
		self._create_rectangle()
		self._create_text(self.string)
		Window.draw(self.rectangle)
		Window.draw(self.text)

	#

	def __init__(self):
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


###################################

from code.level_editor.ui import UIBox
from code.level_editor.ui import InputBox
ui_box = UIBox()
ui_box.position = 100,100
ui_box.add(InputBox, (10,10))
ui_box.add(InputBox, (10,25))

ui_box.add(Button, (20,20))

###################################

Window = Window((1200,600), "UI Box")
from code.sfml_plus import Camera
Camera = Camera(Window)

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed():
			ui_box.center = Camera.center

		ui_box.controls(Window, Key, None)

	Window.clear((255,255,255))
	ui_box.draw(Window, Camera)
	Window.display()