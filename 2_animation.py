from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200,600), "Animation")

##########################################

class Animation(object):
	speed, vel = 0,0
	end = None
	mode = None

	just_passed = False

	def play(self, v):
		self.just_passed = self._just_passed_end(v)
		if self.just_passed:
			self.mode.pass_event(v)

		move = self.speed
		self.speed += self.vel
		return move
	#

	def _just_passed_end(self, v): #play
		if self.end == None: return False
		move = self.speed
		if v <= self.end < v+move: return True
		if v < self.end <= v+move: return True
		if v >= self.end > v+move: return True
		if v > self.end >= v+move: return True
		return False


##### MODES - play
	def __init__(self):
		self.mode = Stop

	_mode = None
	@property
	def mode(self): return self._mode
	@mode.setter
	def mode(self, ModeClass):
		self._mode = ModeClass(self)


class mode:
	def __init__(self, Animation):
		self._ = Animation

	def pass_event(self, v):
		pass

class Stop(mode):
	def pass_event(self, v):
		self._.speed = self._.end - v
		self._.vel = 0

class Bounce(mode):
	def pass_event(self, v):
		self._.speed = -(self._.speed+self._.vel)

class Oscillate(mode):
	def pass_event(self, v):
		self._.vel = -(self._.vel)
		print self._.speed, self._.vel


##########################################

from sfml import Texture
from code.sfml_plus import MySprite

t = Texture.from_file("assets/tilesets/1.png")
sprite = MySprite(t)
sprite.clip.set(25,25)
sprite.position = 200,100

####
Animation = Animation()
Animation.speed = -0
Animation.vel = -0.1
Animation.end = 150
Animation.mode = Oscillate
####

while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed():
			print sprite.x

	sprite.x += Animation.play(sprite.x)
	if Animation.just_passed:
		Animation.speed *= 0.8

	window.clear((255,220,0))
	window.draw(sprite)
	window.display()