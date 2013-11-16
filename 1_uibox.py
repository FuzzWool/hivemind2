from code.sfml_plus import Window
from code.sfml_plus import Key

###################################

from code.level_editor.ui import UIBox
from code.level_editor.ui import InputBox
from code.level_editor.ui import Button

ui_box = UIBox()
ui_box.position = 100,100
ui_box.add(InputBox, (10,10))
ui_box.add(InputBox, (10,25))
ui_box.add(Button, (-5,-5))

###################################

Window = Window((1200,600), "UI Box")

from code.sfml_plus import Mouse
Mouse = Mouse(Window)

from code.sfml_plus import Camera
Camera = Camera(Window)

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed():
			ui_box.center = Camera.center

		ui_box.controls(Window, Key, Mouse)
		if ui_box.events["button_pressed"] != None:
			print "Button pressed."

	Window.clear((255,255,255))
	ui_box.draw(Window, Camera)
	Window.display(Mouse)