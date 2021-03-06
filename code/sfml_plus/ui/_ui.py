from code.sfml_plus import Rectangle
from sfml import Drawable

class _UI(Drawable, Rectangle):
# Communication

	#################################
	# PUBLIC
	# The parent controls the children's controls.

	size_cap = True
	follow = True
	children = []

	def __init__(self):
		self.size_cap = True
		self.follow = True
		self.children = []
		self.previous = Rectangle()

	def controls(self, Key, Mouse, Camera):
		for child in self.children:
			if child.inside(self) and self.size_cap:
				child.controls(Key, Mouse, Camera)
			if not self.size_cap:
				child.controls(Key, Mouse, Camera)

	def draw(self, target, states):
		self._children_position()
		self._children_alpha()
		for child in self.children:
			target.draw(child)

	#################################
	# PRIVATE
	# The parent moves and the children then follow.
	# Also, changes the children's alpha.

	old_pos = 0,0
	old_size = 0,0
	def _children_position(self): #draw
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		for child in self.children:
			if child.follow:
				child.x += x_move
				child.y += y_move
		self.old_pos = self.position
		self.old_size = self.size

	alpha = 255
	def _children_alpha(self):
		for child in self.children:
			if child.follow:
				child.alpha = self.alpha