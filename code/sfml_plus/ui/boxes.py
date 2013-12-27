from code.sfml_plus.ui import _UI
#
from code.sfml_plus import Rectangle
from code.sfml_plus import TweenRectangle
from sfml import RectangleShape, Color


class Box(TweenRectangle, _UI):
# Graphics
# * A raised box with a shadow.
# Events
# * Fancily opens and closes.

	alpha = 255
	_alpha_move = 0

	##### EVENTS
	# Sets up movements and transparency for animation.

	def open(self):
		self.alpha = 0
		self._alpha_move = +30
		self.tween.y -= 20

	def close(self):
		self.alpha = 255
		self._alpha_move = -30
		self.tween.y += 20

	#

	def draw(self, target, states):
		self._play()
		box = self.box()
		shadow = self.shadow()
		self._update_alpha(box,shadow)
		target.draw(box)
		target.draw(shadow)
		#
		_UI.draw(self, target, states)

	####################


	##### GRAPHICS
	# Creates boxes each loop in order to position them.

	w,h = 300,200
	box_fill = Color.WHITE
	box_outline = Color.BLACK

	rise = 5
	@property
	def rise_offset(self): return self.rise-self.old_rise

	#

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


	##### ANIMATION
	# Saves an alpha, forces the graphics to use it.
	# The children refresh their positions to keep up.

	def __init__(self):
		_UI.__init__(self)
		TweenRectangle.__init__(self)

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