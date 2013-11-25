from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Camera

from code.sfml_plus.graphics import Font, Text
from sfml import Color

Window = Window((1200,600), "Text Class")
Camera = Camera(Window)
Camera.zoom = 2
Camera.position = 0,0

Font = Font("speech")
Text = Text(Font)
Text.write("Hello, my name is Sam. I love you!")
Text.center = Camera.center

while Window.is_open:
	if Window.is_focused:

		if Key.ENTER.pressed():
			# Text.letters[0].color = Color(0,0,0,100)
			Text.color = Color(0,0,0,100)

		# x = 0
		# for Letter in Text.letters:
		# 	Letter.x += x
		# 	Letter.y += x
		# 	x += 0.01
		# Text.center = Camera.center


	Window.view = Camera
	Window.clear((255,255,255))
	Window.draw(Text)
	Window.display()