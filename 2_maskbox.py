from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
##########################################

from code.sfml_plus.ui import Box
from sfml import RenderTexture, Color, Sprite

class MaskBox(Box):
# GRAPHICS
# * A box with all of contents drawn to a mask.

	#################################
	# PUBLIC

	def __init__(self):
		Box.__init__(self)
		self._create_Mask()

	def draw(self, target, states):
		self._update_Mask()
		Box.draw(self, self.Mask, states)
		self._draw_Mask(target, states)

	#################################
	# PRIVATE

	Mask = None

	def _create_Mask(self): #init, update_mask
		self.Mask = RenderTexture(self.w+2, self.h+2+self.rise)
		self.Mask.view.reset\
		((self.x-1,self.y-1,self.w+2,self.h+2+self.rise))

	def _update_Mask(self): #draw
		if self.old_pos != self.position\
		or self.old_size != self.size:
			self._create_Mask()
		self.Mask.clear(Color.WHITE)

	def _draw_Mask(self, target, states): #draw
		Mask_sprite = Sprite(self.Mask.texture)
		Mask_sprite.position = self.position
		self.Mask.display()
		target.draw(Mask_sprite)

##########################################

from code.sfml_plus.ui import Box
from code.sfml_plus.ui import Accept_Button, Cancel_Button
# from code.sfml_plus.ui import Slider

Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = MaskBox()
box1.w += 100; box1.h += 100
box1.center = Window.center

box2 = Accept_Button()
box2.x += box1.w - box2.w
box2.y += (box1.h - box2.h) - box2.rise
box1.children.append(box2)

box3 = Cancel_Button()
box3.x += box1.w - (box3.w*2)
box3.y += (box1.h - box3.h) - box3.rise
box3.y += 15
box1.children.append(box3)

##########################################

while Window.is_open:
	if Window.is_focused:

		# if box2.selected\
		# or Key.BACKSPACE.pressed():
		# 	box1.close()

		if Key.ENTER.pressed():
			box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display(Mouse)