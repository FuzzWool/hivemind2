class Animation(object):
	speed, vel = 0,0
	end = None
	mode = None

	just_passed = False

	def play(self, v):

		self.mode.passive(v)

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

	def passive(self, v): pass
	def pass_event(self, v): pass

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

class Magnet(Stop):
	saved_speed = 0

	def passive(self, v):
		#save the speed when moving
		if self._.speed != 0:
			self.saved_speed = self._.speed

		#move when not at the end
		if v != self._.end:
			if self.saved_speed != 0:
				self._.speed = self.saved_speed

		#move towards end, reverse
		if self._.end < v:
			self._.speed = -abs(self._.speed)
		if self._.end > v:
			self._.speed = +abs(self._.speed)