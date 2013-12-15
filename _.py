from code.sfml_plus import Window
from code.sfml_plus import Key

#######################################

from code.sfml_plus import Texture, MySprite
from sfml import Color

t = Texture.from_file("assets/tilesets/1.png")
s = MySprite(t)

s.color = Color(255,255,255,-100)


#######################################

Window = Window((1200,600), "Untitled")

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Window.draw(s)
	Window.display()