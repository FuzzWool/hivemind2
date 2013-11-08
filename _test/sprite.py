from code.sfml_plus import Window
from code.sfml_plus import key

window = Window((1200,600), "MySprite")

from sfml import Texture
from code.sfml_plus import MySprite

t = Texture.from_file("assets/tilesets/1.png")
sprite = MySprite(t)
sprite.position = 100,100

sprite.clip.set(25,25)
sprite.clip.use(0,0)


while window.is_open:
	if window.is_focused:
		if key.ENTER.pressed():
			pass

	window.clear((255,220,0))
	window.draw(sprite)
	window.display()