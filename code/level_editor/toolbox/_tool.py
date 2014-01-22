from code.sfml_plus.ui import Box, Button
from code.sfml_plus import Texture, MySprite
from code.sfml_plus import Font, Text
from code.sfml_plus.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from sfml import Color


class _Tool(Button):
# GRAPHICS
	# * A tile-shape.
# LOGIC
	# * 'Selected' state controlled externally.
	#	 Has special 'active' controls for it.


	#################################
	# PUBLIC

	texture_clip = 0
	w,h = 80,50

	help_text = "I'm a work-in-progress tool!"

	open_error = False
	error_text = ""
	
	parent_states = None
	active = False


	class deactive_colors:
		normal_color = Color(240,240,240)
		hovered_color = Color(255,255,255)
		held_color = hovered_color
		selected_color = hovered_color

	class active_colors:
		normal_color = Color(240,240,240)
		hovered_color = Color(255,255,255)
		held_color = hovered_color
		selected_color = hovered_color

	#

	def __init__(self):
		Button.__init__(self)
		self.text = ""
		self.active = False
		self._init_sprite()

	def controls(self, Key, Mouse, Camera):
		Button.controls(self, Key, Mouse, Camera)
		self._Key = Key
		self._Mouse = Mouse
		self._Camera = Camera

		self._help_state(Mouse)
		self._open_help()
		self._open_Error()


	def add_controls(self, WorldMap):
		pass

	def normal_draw(self, target, states):
		pass

	def static_draw(self, target, states):
		self._apply_coloring()
		Button.draw(self, target, states)
		self._draw_sprite(target, states)
		self._draw_help(target, states)
		self._draw_Error(target, states)

	#

	def open(self):
	#Create all windows for the Tool.
		self.active = True

	def close(self):
	#Close all windows for the Tool.
		self.active = False


	#################################
	# PRIVATE

	###
	# Color

	def _init_coloring(self):
		self.active_colors = self.active_colors()
		self.deactive_colors = self.deactive_colors()

	def _apply_coloring(self):
		if self.active: group = self.active_colors
		if not self.active: group = self.deactive_colors
		#
		self.box_fill = group.normal_color
		if self.hovered:
			self.box_fill = group.hovered_color
		if self.held:
			self.box_fill = group.held_color
		if self.selected:
			self.box_fill = group.selected_color

	###
	#Sprite

	def _init_sprite(self):
		texture = Texture.from_file("assets/ui/tools.png")
		self.sprite = MySprite(texture)
		self.sprite.clip.set(80,50)
		self.sprite.clip.use(self.texture_clip, 0)

	def _draw_sprite(self, target, states):
		self.sprite.center = self.center
		self.sprite.y -= self.rise_offset
		target.draw(self.sprite, states)


	###
	# Help

	#help_text
	_help = False
	_HelpBox = None


	def _help_state(self, Mouse): #controls
		if Mouse.inside(self) and self.active:
			self._help = True
		else:
			self._help = False

	def _open_help(self): #controls
		if self._help == True:
			if self._HelpBox == None: self._create_help()
			self._HelpBox.open()
		if self._help == False:
			if self._HelpBox != None:
				if self._HelpBox.alpha > 0:
					self._HelpBox.close()
				else:
					self._HelpBox = None

	def _draw_help(self, target, states): #draw
		if self._HelpBox != None:
			target.draw(self._HelpBox, states)

	#

	def _create_help(self): #_open_help
		self._HelpBox = Box()
		Text1 = Text(Font("speech"))
		Text1.x += 5; Text1.y += 5
		Text1.write(self.help_text)
		self._HelpBox.size = Text1.w+20, Text1.h+20
		self._HelpBox.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
		self._HelpBox.children.append(Text1)

	###
	# Error

	# open_error = False
	# error_text = ""
	_ErrorBox = None


	def _open_Error(self): #controls
		if self.open_error:
			if self._ErrorBox == None:
				self._create_Error()
				self._ErrorBox.open()
		else:
			if self._ErrorBox != None:
				self._ErrorBox.close()
				if self._ErrorBox.alpha == 0:
					del self._ErrorBox

		self.open_error = False

	def _draw_Error(self, target, states): #draw
		if self._ErrorBox != None:
			target.draw(self._ErrorBox, states)
	
	#

	def _create_Error(self): #_open_Error
		self._ErrorBox = Box()
		Text1 = Text(Font("speech"))
		Text1.write(self.error_text)
		Text1.x += 5; Text1.y += 5
		self._ErrorBox.size = Text1.w+10, Text1.h+10
		self._ErrorBox.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
		self._ErrorBox.children.append(Text1)