from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
##########################################

from code.sfml_plus.ui import Box
from code.sfml_plus.ui import Accept_Button, Cancel_Button
from code.sfml_plus.ui import Horizontal_Slider, Vertical_Slider, SliderBox
# from code.sfml_plus.ui import Slider

Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()
box1.w += 100; box1.h += 100
box1.center = Window.center

box2 = Accept_Button()
box2.x += box1.w - box2.w
box2.y += (box1.h - box2.h) - box2.rise
box1.children.append(box2)

box3 = Cancel_Button()
box3.x += box1.w - (box3.w*2)
box3.y += (box1.h - box3.h) - box3.rise
box1.children.append(box3)

#

sliderbox = SliderBox()
sliderbox.x += (box1.w/2) - (sliderbox.w/2)
sliderbox.y += (box1.h/2) - (sliderbox.h/2)
sliderbox.y -= 20
box1.children.append(sliderbox)

sbox1 = Accept_Button()
sbox1.x += 5; sbox1.y += 5
sliderbox.Box.children.append(sbox1)

sbox2 = Cancel_Button()
sbox2.x += 5; sbox2.y += 800
sliderbox.Box.children.append(sbox2)

#

# slider = Vertical_Slider()
# slider.lines = 2
# box1.children.append(slider)

##########################################

while Window.is_open:
	if Window.is_focused:

		if box2.selected\
		or Key.BACKSPACE.pressed():
			box1.close()

		if Key.ENTER.pressed():
			box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display(Mouse)