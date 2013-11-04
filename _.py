import sfml as sf

v = sf.VideoMode(1200,600)
window = sf.RenderWindow(v, "window")

pressed = False
while window.is_open:


	####

	old_pressed = pressed
	pressed = False
	if sf.Keyboard.is_key_pressed(sf.Keyboard.SUBTRACT):
		pressed = True 

	if pressed != old_pressed:
		print "Just pressed/released."

	####

	for event in window.events:
		if type(event) is sf.CloseEvent: window.close()

	window.clear(sf.Color(255,220,0))
	window.display()