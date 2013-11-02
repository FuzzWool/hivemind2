from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200, 600), "Hivemind - Demo 2")

from code.game import WorldMap
WorldMap = WorldMap(2,2)

while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed():
			pass

	window.clear((255,220,0))
	WorldMap.draw(window)
	window.display()