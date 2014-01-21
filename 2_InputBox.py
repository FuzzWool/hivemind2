from code.sfml_plus import Window
from code.sfml_plus import Key
################################################
from code.sfml_plus.ui import InputBox, Box

################################################

Window = Window((1200,600), "InputBox")
box1 = Box()
box1.position = 200,200
box1.open()

InputBox1 = InputBox()
InputBox1.position = 5,5
box1.children.append(InputBox1)

while Window.is_open:
	if Window.is_focused:
		box1.controls(Key, None, None)

		if Key.ENTER.pressed():
			print InputBox1.text

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display()