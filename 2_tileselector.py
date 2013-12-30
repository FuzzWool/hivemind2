from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus import Mouse

##########################################

from code.sfml_plus.ui import Box
from code.sfml_plus import Texture, MySprite
from code.sfml_plus import Rectangle

class TileSelector(Box):
	
	#################################
	# PUBLIC

	def __init__(self):
		Box.__init__(self)
		self.Sheet = self.Sheet("0.png")
		self.size = self.Sheet.size

	def draw(self, target, states):
		self._parent_Sheet()
		Box.draw(self, target, states)
		self.Sheet.draw(target, states)

	#################################
	# PRIVATE

	# SHEET
	def _parent_Sheet(self):
		#alpha
		self.Sheet.alpha = self.alpha
		#move
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		self.Sheet.x += x_move
		self.Sheet.y += y_move


	class Sheet(Rectangle):

		def __init__(self, name):
			Rectangle.__init__(self)
			self._create_sprite(name)

		def draw(self, target, states):
			self._parent_sprite()
			self._draw_sprite(target, states)
		#

		_sprite = None
		def _create_sprite(self, name):
			t = Texture.from_file("assets/tilesheets/"+name)
			self._sprite = MySprite(t)
			self.size = self._sprite.size
		#
		def _parent_sprite(self):
			c = self._sprite.color
			c.a = self.alpha
			self._sprite.color = c
			self._sprite.position = self.position
		def _draw_sprite(self, target, states):
			target.draw(self._sprite)



##########################################


from code.sfml_plus.ui import Box
from code.sfml_plus.ui import Accept_Button, Cancel_Button

Window = Window((1200,600), "Untitled")
Mouse = Mouse(Window)

box1 = Box()
box1.w += 250; box1.h += 100
box1.center = Window.center

box2 = Accept_Button()
box2.x += box1.w - box2.w
box2.y += (box1.h - box2.h) - box2.rise
box1.children.append(box2)

tileselector = TileSelector()
tileselector.x += 25; tileselector.y += 20
box1.children.append(tileselector)

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