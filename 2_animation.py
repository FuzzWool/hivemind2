from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200,600), "Animation")

##########################################

class Animation:
	speed, vel = 0,0
	end = None

	def play(self, v):
		self.speed += self.vel
		move = self.speed
		if self._just_passed_end(v, move):
			move = self._stop(v, move)

		return move
	#

	def _just_passed_end(self, v, move):
		if self.end == None: return False
		if v <= self.end < v+move: return True
		if v < self.end <= v+move: return True
		if v >= self.end > v+move: return True
		if v > self.end >= v+move: return True
		return False

	def _stop(self, v, move):
		self.speed, self.vel = 0, 0
		return self.end - v

##########################################

from sfml import Texture
from code.sfml_plus import MySprite

t = Texture.from_file("assets/tilesets/1.png")
sprite = MySprite(t)
sprite.clip.set(25,25)
sprite.position = 200,100

####
Animation = Animation()
Animation.speed = -1
Animation.vel = -0.1
Animation.end = 100
####

while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed():
			print sprite.x

	sprite.x += Animation.play(sprite.x)

	window.clear((255,220,0))
	window.draw(sprite)
	window.display()