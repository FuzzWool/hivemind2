from code.sfml_plus import Window
from code.sfml_plus import key

###################################

from code.sfml_plus import Rectangle
class Button(Rectangle):
	
	def controls(self, window, key, mouse):
		pass

	def draw(self, window, camera):
		pass

###################################

from code.level_editor.ui import UIBox
from code.level_editor.ui import InputBox
ui_box = UIBox()
ui_box.position = 100,100
ui_box.add(InputBox, (10,10))
ui_box.add(InputBox, (10,25))

###################################

window = Window((1200,600), "UI Box")
from code.sfml_plus import Camera
Camera = Camera(window)

while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed():
			ui_box.center = Camera.center
		ui_box.controls(window, key, None)

	window.clear((255,255,255))
	ui_box.draw(window, Camera)
	window.display()