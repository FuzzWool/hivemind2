from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus.ui import Box

Window = Window((1200,600), "Untitled")
Box1 = Box()
Box1.open()
Box1.center = 1200/2, 600/2

################################################

from code.sfml_plus.graphics import Font, Text

Text1 = Text(Font("speech"))
Text1.write("Hello.")
Text1.position = Box1.x+10,Box1.y+10

################################################


while Window.is_open:
	if Window.is_focused:
		Box1.controls(None,None,None)
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Window.draw(Box1)
	Window.draw(Text1)
	Window.display()