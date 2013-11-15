from code.sfml_plus import Window
from code.sfml_plus import Key

###################################

from code.sfml_plus import Rectangle
class Button(Rectangle):
	
	def controls(self, Window, Key, Mouse):
		pass

	def draw(self, Window, Camera):
		pass

###################################

from code.level_editor.ui import UIBox
from code.level_editor.ui import InputBox
ui_box = UIBox()
ui_box.position = 100,100
ui_box.add(InputBox, (10,10))
ui_box.add(InputBox, (10,25))

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
	Window.display(Camera)