from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((600,300), "Hivemind - Demo 2")

while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed(): print 1

	window.clear((255,220,0))
	window.display()