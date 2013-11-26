class _Button: #virtual
# . Monitors a 'held' state. Override it.
# * Notes if it has just been pressed or released.
# (Needs to be looped so it refreshes cleanly.)
	
	def held(self): return False

	#

	was_held = False

	_pressed = False
	def pressed(self): return self._pressed

	_released = False
	def released(self): return self._released

	#

	def reset(self): #Must be called at the end of a loop.
		self._pressed =(self.held() and not self.was_held)
		self._released =(not self.held() and self.was_held)
		self.was_held = self.held()