from code.sfml_plus.ui import Box
#
from code.sfml_plus import Font, Text
from sfml import Color

class Button(Box):
# State Handling
# 	* Hovering, Pressing, Selecting
# Graphics
# 	* Rises based on state.
# 	* Colored based on state.
#	* (Optional) contains text.

	w,h = 50,20

	def controls(self,Key, Mouse, Camera):
		self._hover(Mouse)
		self._select(Mouse)
		self._held(Mouse)
		self._color_states()
		Box.controls(self,Key,Mouse,Camera)

	def draw(self, Window):
		Box.draw(self, Window)
		self._draw_Text(Window)


	####################
	### STATE HANDLING

	hovered = False
	held = False
	selected = False

	def _hover(self, Mouse):
		self.hovered = Mouse.inside(self)

	def _held(self, Mouse):
		if Mouse.left.pressed():
			if self.hovered:
				self.held = True
				self.rise = 0
		elif not Mouse.left.held():
			self.held = False
			self.rise = self.old_rise

	def _select(self, Mouse):
		self.selected = False
		if not Mouse.left.held():
			if self.held:
				self.selected = True


	### COLORING

	box_fill = Color(240,240,240)
	old_fill = box_fill
	hovered_color = Color(255,255,255)
	held_color = hovered_color
	selected_color = hovered_color

	def _color_states(self):
		self.box_fill = self.old_fill
		if self.hovered:
			self.box_fill = self.hovered_color
		if self.held:
			self.box_fill = self.held_color
		if self.selected:
			self.box_fill = self.selected_color


	### TEXT (Optional)
	# Create, pos/alpha, draw

	_Text = Text(Font("speech"))
	text = ""
	_text = text

	def _draw_Text(self, Window):
		#update text
		if self._text != self.text:
			self._Text.write(self.text)
		#color
		text = self._Text
		c=text.color;c.a=self.alpha;text.color=c
		#pos
		text.center = self.center
		text.y -= self.rise_offset
		#draw
		Window.draw(text)



####

class Cancel_Button(Button):
# Graphics - colors/text

	hovered_color = Color(255,150,150)
	held_color = Color.RED
	selected_color = Color.RED
	text = "Nah"

class Accept_Button(Button):
	hovered_color = Color(150,255,150)
	held_color = Color.GREEN
	selected_color = Color.GREEN
	text = "Sure"