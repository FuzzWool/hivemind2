from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200,600), "Animation")

##########################################

from code.sfml_plus import Animation
from code.sfml_plus.animation import Oscillate

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
			pass

	sprite.x += Animation.play(sprite.x)
	if Animation.just_passed:
		Animation.speed *= 0.8

	window.clear((255,220,0))
	window.draw(sprite)
	window.display()