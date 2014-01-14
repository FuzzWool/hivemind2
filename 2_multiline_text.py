from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus.ui import Box

Window = Window((1200,600), "Untitled")
Box1 = Box()
Box1.size = 300,300
Box1.open()
Box1.center = 1200/2, 600/2

################################################

from sfml import Drawable
from code.sfml_plus.graphics import Font, Text
from code.sfml_plus.graphics import Rectangle

class Multiline_Text(Drawable, Rectangle):

	#################################
	# PUBLIC

	###
	#Core

	x,y,w,h = 0,0,0,0
	Font = None
	padding = 10

	def __init__(self, Font):
		self.Font = Font

	def draw(self, target, states):
		self._draw_Text_rows(target, states)

	###
	# Writing Styles

	def write(self, text):
		self._create_Text_rows(text)

	def say(self, text):
		pass


	#################################
	# PRIVATE

	###
	# Text Rows

	_Text_rows = []

	def _create_Text_rows(self, t): #write

		def new_row(text):
			#Create a Text row.
			new_row = Text(self.Font)
			new_row.write(text)
			new_row.position = self.x+self.padding, self.y+self.padding
			return new_row

		def new_index(text):
			#Find all the spaces in the string (word indexing).
			def find(string, wanted_char):
				for i, char in enumerate(string):
					if char == wanted_char:
						yield i
			return list(find(text, " "))


		def add_rows(text):
			#Create a new row each time the last exceeds the width.
			row = new_row(text)
			index = new_index(text)
			old_i = 0
			broken = False

			for i in index:
				w = row.letters[i].x2 - row.letters[0].x1
				max_w = self.w - self.padding
				if w > max_w:
					row.write(text[:old_i])
					self._Text_rows.append(row)
					add_rows(text[old_i+1:])
					broken = True; break
				old_i = i

			if not broken:
				row.write(text)
				self._Text_rows.append(row)


		self._Text_rows = []
		# add_rows(t)
		sentences = t.split("\n")
		for line in sentences:
			add_rows(line)

		#adjust height
		for i, row in enumerate(self._Text_rows):
			row.y += i*row.h


	def _draw_Text_rows(self, target, states): #draw
		for row in self._Text_rows:
			target.draw(row, states)



################################################

Text1 = Multiline_Text(Font("speech"))
Text1.position = Box1.position
Text1.size = Box1.size
Text1.padding = 5
Text1.write("Hmm. Sam. Yes, my name is Sam. Hmmm. Not very well optimized, hmm. Hmmm. Yes. \n\n HE THREW IT IN THE TRASH. LET'S A GO. WAAA HA HA. HAAAAA.\n\n "*3)

while Window.is_open:
	if Window.is_focused:
		Box1.controls(None,None,None)
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Window.draw(Box1)
	Window.draw(Text1)
	Window.display()