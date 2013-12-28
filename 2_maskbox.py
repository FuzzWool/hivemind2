from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse
##########################################

from code.sfml_plus.ui import Box
from code.sfml_plus import Rectangle
from sfml import RenderTexture, Color, Sprite

class MaskBox(Box):
# GRAPHICS
# * Mask - only renders graphics inside of the box.
# * Offset - moves, and remembers the size of, all the children.

	#################################
	# PUBLIC

	def __init__(self):
		Box.__init__(self)
		self._create_Mask()
		self.offset = self.offset(self)

	def draw(self, target, states):
		#MASK
		self._update_Mask()
		Box.draw(self, self.Mask, states)
		self._draw_Mask(target, states)

	#################################
	# PRIVATE

	# MASK
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

	# OFFSET
	class offset(Rectangle):
	#Proportional movements. NOT absolute.
		def __init__(self, MaskBox):
			self._ = MaskBox

		# Position - public
		# Move all of the children inside the box.
		_x,_y = 0,0
		@property
		def x(self): return self._x
		@x.setter
		def x(self, x):
			move = x - self._x
			for child in self._.children:
				child.x += move
			self._x = x
		@property
		def y(self): return self._y
		@y.setter
		def y(self, y):
			move = y - self._y
			for child in self._.children:
				child.y += move
			self._y = y

		# Size - read only
		# Work out the size of the box by child distance.
		@property
		def w(self):
			if len(self._.children) == 0: return self._.size
			#
			x1 = self._.x1
			x2 = None
			for child in self._.children:
				if x2 == None: x2 = child.x2
				if child.x2 > x2: x2 = child.x2
			x2 -= self.x
			w = x2 - x1
			if self._.w > w: w = self._.w
			return w

		@property
		def h(self):
			if len(self._.children) == 0: return self._.size
			#
			y1 = self._.y1
			y2 = None
			for child in self._.children:
				if y2 == None: y2 = child.y2
				if child.y2 > y2: y2 = child.y2
			y2 -= self.y
			h = y2 - y1
			if self._.h > h: h = self._.h
			return h

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
box1.children.append(box3)

##########################################

while Window.is_open:
	if Window.is_focused:

		if Key.ENTER.pressed():
			box1.offset.y += 10
			print box1.offset.size

		# if box2.selected\
		# or Key.BACKSPACE.pressed():
		# 	box1.close()

		# if Key.ENTER.pressed():
		# 	box1.open()

		box1.controls(Key, Mouse, None)

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display(Mouse)