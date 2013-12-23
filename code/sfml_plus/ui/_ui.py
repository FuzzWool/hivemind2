from code.sfml_plus import Rectangle

class _UI(Rectangle):
# Communication

	### LOGIC
	# The parent controls the children's controls.

	def __init__(self):
		self.children = []

	def controls(self, Key, Mouse, Camera):
		for child in self.children:
			child.controls(Key, Mouse, Camera)

	def draw(self, Window):
		self._children_position()
		self._children_alpha()
		for child in self.children:
			child.draw(Window)


	### GRAPHICS
	# The parent moves and the children then follow.
	# Also, changes the children's alpha.

	old_pos = 0,0
	def _children_position(self): #draw
		x_move = self.x - self.old_pos[0]
		y_move = self.y - self.old_pos[1]
		for child in self.children:
			child.x += x_move
			child.y += y_move
		self.old_pos = self.position

	alpha = 255
	def _children_alpha(self):
		for child in self.children:
			child.alpha = self.alpha