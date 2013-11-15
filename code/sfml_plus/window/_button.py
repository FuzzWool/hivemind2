class _Button: #virtual
# . Monitors a 'held' state. Override it.
# * Notes if it has just been pressed or released.
# (Needs to be looped so it refreshes cleanly.)
	
	def held(self): return False

	#

	was_pressed = False
	def pressed(self):
		if self.held() and not self.was_pressed:
			return True
		return False

	def released(self):
		if not self.held() and self.was_pressed:
			return True
		return False

	#

	def reset(self): #Must be called at the end of a loop.
		self.was_pressed = self.held()