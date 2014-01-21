from code.sfml_plus import Window
from code.sfml_plus import Key
################################################
from code.sfml_plus.ui import _UI, Box
from code.sfml_plus import Font, Text

#Cursor
from sfml import RectangleShape, Color
from sfml import Clock

class InputBox(Box):
#Keyboard-typed text is added to this box.

	#################################
	# PUBLIC
	
	text = None
	w,h = 200,20
	
	def __init__(self):
		Box.__init__(self)
		self._init_Text()
		self._init_Cursor()

	def controls(self, Key, Mouse, Camera):
		Box.controls(self, Key, Mouse, Camera)
		self._write_Text(Key)
		self._move_Cursor()

	#################################
	# PRIVATE
	
	###
	# Text

	_Text = None

	def _init_Text(self):
		self._Text = Text(Font("speech"))
		self._Text.write("")
		self._Text.position = 5,5
		def filler(a1,a2,a3): pass
		self._Text.controls = filler
		self.children.append(self._Text)

	def _write_Text(self, Key):
		#Add/remove a letter.
		alphabet = ["A","B","C","D","E","F","G","H","I","J","K",
		"L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
		if Key.pressed in alphabet:
			letter = Key.pressed.lower()
			if Key.L_SHIFT.held(): letter = letter.upper()
			self._Text.write(self._Text.string+letter)
		if Key.pressed == "BACKSPACE":
			if len(self._Text.string) >= 1:
				self._Text.write(self._Text.string[:-1])
		if Key.pressed == "SPACE":
			self._Text.write(self._Text.string+"-")

		#Keep text in bounds.
		if self._Text.x2+5 > self.x2:
			self._Text.write(self.text)
		self.text = self._Text.string


	###
	# Cursor

	_Cursor = None

	def _init_Cursor(self):
		self._Cursor = self.Cursor()
		self._Cursor.position = 2, 3
		self.children.append(self._Cursor)

	def _move_Cursor(self):
		self._Cursor.x = self._Text.x2

	class Cursor(_UI):
	# A blinking line.
		
		#################################
		# PUBLIC

		def __init__(self):
			_UI.__init__(self)
			self._init_Box()

		def draw(self, target, states):
			self._parent_Box(target, states)
			self._flicker_Box()
			_UI.draw(self, target, states)
			self._draw_Box(target, states)

		#################################
		# PRIVATE

		w,h = 2,15
		_Box = None
		_Flicker_Clock = None

		def _init_Box(self):
			self._Box = RectangleShape(self.size)
			self._Flicker_Clock = Clock()
			self._Box.fill_color = Color.BLACK

		def _parent_Box(self, target, states):
			x_move = self.x - self.old_pos[0]
			y_move = self.y - self.old_pos[1]
			self._Box.position = \
			self._Box.position[0]+x_move, self._Box.position[1]+y_move

		def _draw_Box(self, target, states):
			self._Box.draw(target, states)

		def _flicker_Box(self):
			if self._Flicker_Clock.elapsed_time.seconds >= 0.5:
				if self._Box.fill_color.a != 0:
					c=self._Box.fill_color;c.a=0;self._Box.fill_color=c
				else:
					a = self.alpha
					c=self._Box.fill_color;c.a=a;self._Box.fill_color=c
				self._Flicker_Clock.restart()


################################################

Window = Window((1200,600), "InputBox")
box1 = Box()
box1.position = 200,200
box1.open()

InputBox1 = InputBox()
InputBox1.position = 5,5
box1.children.append(InputBox1)

while Window.is_open:
	if Window.is_focused:
		box1.controls(Key, None, None)

		if Key.ENTER.pressed():
			print InputBox1.text

	Window.clear((255,220,0))
	Window.draw(box1)
	Window.display()