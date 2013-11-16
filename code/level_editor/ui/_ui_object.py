from code.sfml_plus import Rectangle

class _ui_object(Rectangle):

	def __init__(self, id):
		self.id = id

	def controls(self, events, Window, Key, Mouse):
		pass

	def draw(self, Window, Camera):
		pass
