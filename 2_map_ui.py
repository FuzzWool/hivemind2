from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

##################################################
from code.sfml_plus import Rectangle, TweenRectangle, RectangleShape
from sfml import Drawable, Color
from sfml import RenderTexture, Sprite
from code.sfml_plus.constants import ROOM_WIDTH, ROOM_HEIGHT

class _UI(TweenRectangle, Drawable):
# Communication
# GRAPHICS
	# * Designed to be Tweened and Drawn.
# LOGIC
	# * Children follow positioning and alpha.

	##############################
	# PUBLIC

	children = []

	def __init__(self):
		TweenRectangle.__init__(self)
		Drawable.__init__(self)
		self.children = []
		self._create_Mask()
		self.previous = Rectangle()

	def controls(self, Key, Mouse, Camera):
		self._children_controls(Key, Mouse, Camera)

	def draw(self, target, states):
		self.tween.play()
		self._update_Mask()
		self.mask_draw(target, states)
		self._draw_Mask(target, states)
		self.nonmask_draw(target, states)
		self.previous.points = self.points

	##############################
	# CHILDREN

	def mask_draw(self, target, states):
		pass

	def nonmask_draw(self, target, states):
		pass

	###############################
	# PRIVATE	
	
	# Children
	def _children_controls(self): #controls
		for child in self.children:
			child.controls(Key, Mouse, Camera)

	def _children_draw(self, target, states): #draw
		for child in self.children:
			pass


	# Mask
	Mask = None

	def _create_Mask(self): #init
		self.Mask = RenderTexture(self.w+2, self.h+2)
		self.Mask.view.reset((self.x-1,self.y-1,self.w+2,self.h+2))

	def _update_Mask(self): #draw
		if self.previous.points != self.points:
			self._create_Mask()
		self.Mask.clear(Color.WHITE)

	def _draw_Mask(self, target, states): #draw
		Mask_sprite = Sprite(self.Mask.texture)
		Mask_sprite.position = self.position
		self.Mask.display()
		target.draw(Mask_sprite)


class Box(_UI):
# GRAPHICS
# * Layers - of rectangles. The top and the base.
	
	##############################
	# LOCAL

	_w,_h = 200,200
	children = []

	def __init__(self):
		_UI.__init__(self)
		self._create_Box()

	def draw(self, target, states):
		self.Box.points = self.points
		_UI.draw(self, target, states)


	##############################
	# WIP - Masking for UI

	def mask_draw(self, target, states):
		self.Mask.draw(self.Box)

	def nonmask_draw(self, target, states):
		pass# target.draw(self.Box)


	##############################
	# PRIVATE

	def _create_Box(self):
		self.Box = RectangleShape()
		self.Box.points = self.points
		self.Box.outline_thickness = 1
		self.Box.outline_color = Color.BLACK


##################################################

Window = Window((1200,600), "MAP (Mask, Alpha, Position) UI")
Mouse = Mouse(Window)

Box1 = Box()
Box1.position = 50,50

Box2 = Box()
Box2.position = 50,50
Box2.size = 10,10
Box1.children.append(Box2)

while Window.is_open:
	if Window.is_focused:
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Window.draw(Box1)
	Window.display(Mouse)