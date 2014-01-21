from code.sfml_plus.ui import _UI
#
from code.sfml_plus import Rectangle
from code.sfml_plus import TweenRectangle
from sfml import RectangleShape, Color

from sfml import RenderTexture, Sprite


class Box(TweenRectangle, _UI):
# Graphics
# * A raised box with a shadow.
# Events
# * Fancily opens and closes.

	alpha = 0
	_alpha_move = 0

	#################################
	# PUBLIC

	opened = False

	def __init__(self):
		_UI.__init__(self)
		TweenRectangle.__init__(self)
		self.opened = False
		self.alpha = 0

	def draw(self, target, states):
		self._play()
		self.draw_self(target, states)
		self.draw_children(target, states)

	#

	def draw_self(self, target, states):
		box = self.box()
		shadow = self.shadow()
		self._update_alpha(box,shadow)
		target.draw(box)
		target.draw(shadow)

	def draw_children(self, target, states):
		_UI.draw(self, target, states)

	#

	def open(self):
		if self.opened == False:
			self.opened = True
			self.alpha = 0
			self._alpha_move = +30
			self.tween.y -= 20

	def close(self):
		if self.opened == True:
			self.opened = False
			self.alpha = 255
			self._alpha_move = -30
			self.tween.y += 20


	#################################
	# PRIVATE


	# GRAPHICS
	# Creates boxes each loop in order to position them.

	w,h = 300,200
	box_fill = Color.WHITE
	box_outline = Color.BLACK

	rise = 5
	@property
	def rise_offset(self): return self.rise-self.old_rise

	old_rise = rise
	def box(self): #draw
		size = self.w, self.h+self.rise
		b = RectangleShape(size)
		b.position = self.x, self.y-self.rise_offset
		b.outline_thickness = 1
		b.outline_color = self.box_outline
		b.fill_color = self.box_fill
		return b

	def shadow(self): #draw
		w,h = self.size
		b = RectangleShape((w,self.rise))
		b.position = self.x, self.y2
		b.fill_color = Color(0,0,0,255)
		return b


	# ANIMATION
	# Saves an alpha, forces the graphics to use it.
	# The children refresh their positions to keep up.

	def _play(self): #draw
		self.tween.play()

	def _update_alpha(self, box,shadow): #draw
		self._change_alpha()
		self._update(box,shadow)

	#

	def _change_alpha(self):
		a, amt = self.alpha, self._alpha_move
		if a + amt < 0: a = 0
		elif a + amt > 255: a = 255
		else: a += amt
		self.alpha = a

	def _update(self, box,shadow):
		a=self.alpha
		c=box.fill_color;c.a=a;box.fill_color=c
		c=box.outline_color;c.a=a;box.outline_color=c
		c=shadow.fill_color;c.a=a/4;shadow.fill_color=c



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

	def _create_Mask(self): #init
		self.Mask = RenderTexture(self.w+2, self.h+2+self.rise)

	def _update_Mask(self): #draw
		if self.old_pos != self.position\
		or self.old_size != self.size:
			self.Mask.view.reset\
			((self.x-1,self.y-1,self.w+2,self.h+2+self.rise))
		color = self.box_fill; color.a = 0
		self.Mask.clear(color)

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


################################################
################################################
################################################
################################################


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
