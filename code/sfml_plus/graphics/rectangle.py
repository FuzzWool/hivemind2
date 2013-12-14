from code.sfml_plus.constants import TILE as T
from code.sfml_plus.constants import ROOM_WIDTH as RX
from code.sfml_plus.constants import ROOM_HEIGHT as RY

class Rectangle(object):

	#### ABSOLUTE
	_origin = 0,0
	_x,_y,_w,_h = 0,0,0,0

	@property
	def origin(self): return self._origin
	@origin.setter
	def origin(self, o):
		self._origin = o
		self.position = self.position

	@property
	def x(self): return self._x - self.origin[0]
	@x.setter
	def x(self,x): self._x = x + self.origin[0]
	@property
	def y(self): return self._y - self.origin[1]
	@y.setter
	def y(self,y): self._y = y + self.origin[1]
	@property
	def w(self): return self._w
	@w.setter
	def w(self,w): self._w = w
	@property
	def h(self): return self._h
	@h.setter
	def h(self,h): self._h = h



	# x1, y1, x2, y2
	# position
	# size
	# points
	# center


	#x1
	@property
	def x1(self): return self.x
	@x1.setter
	def x1(self, x1): self.x = x1
	#
	#y1
	@property
	def y1(self): return self.y
	@y1.setter
	def y1(self, y1): self.y = y1
	#
	#x2
	@property
	def x2(self): return self.x + self.w
	@x2.setter
	def x2(self, x2): self.w = x2 - self.x
	#
	#y2
	@property
	def y2(self): return self.y + self.h
	@y2.setter
	def y2(self, y2): self.h = y2 - self.y


	#position
	@property
	def position(self): return self.x, self.y
	@position.setter
	def position(self, args): self.x, self.y = args

	#size
	@property
	def size(self): return self.w, self.h
	@size.setter
	def size(self, args): self.w, self.h = args

	#points
	@property
	def points(self):
		return self.x1,self.y1,self.x2,self.y2
	@points.setter
	def points(self,args):
		self.x1,self.y1,self.x2,self.y2 = args

	#center
	@property
	def center(self):
		return self.x+(self.w/2), self.y+(self.h/2)
	@center.setter
	def center(self,a):
		self.x,self.y = a[0]-(self.w/2),a[1]-(self.h/2)


	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	#### TILE
	
	#x
	@property
	def tile_x(self): return int(self.x/T)
	@tile_x.setter
	def tile_x(self,x): self.x = x*T
	#
	#y
	@property
	def tile_y(self): return int(self.y/T)
	@tile_y.setter
	def tile_y(self,y): self.y = y*T
	#
	#w
	@property
	def tile_w(self): return int(self.w/T)
	@tile_w.setter
	def tile_w(self,w): self.w = w*T
	#
	#h
	@property
	def tile_h(self): return int(self.h/T)
	@tile_h.setter
	def tile_h(self,h): self.h = h*T

	####

	#x1
	@property
	def tile_x1(self): return self.tile_x
	@tile_x1.setter
	def tile_x1(self, x1): self.tile_x = x1
	#
	#y1
	@property
	def tile_y1(self): return self.tile_y
	@tile_y1.setter
	def tile_y1(self, y1): self.tile_y = y1
	#
	#x2
	@property
	def tile_x2(self): return self.tile_x + self.tile_w
	@tile_x2.setter
	def tile_x2(self, x2): self.tile_x = x2 - self.tile_w
	#
	#y2
	@property
	def tile_y2(self): return self.tile_y + self.tile_h
	@tile_y2.setter
	def tile_y2(self, y2): self.tile_y = y2 - self.tile_h


	#position
	@property
	def tile_position(self):
		return self.tile_x, self.tile_y
	@tile_position.setter
	def tile_position(self, args):
		self.tile_x, self.tile_y = args

	#size
	@property
	def tile_size(self): return self.tile_w, self.tile_h
	@tile_size.setter
	def tile_size(self, args):
		self.tile_w, self.tile_h = args

	#points
	@property
	def tile_points(self):
		return self.tile_x1,self.tile_y1,\
		self.tile_x2,self.tile_y2
	@tile_points.setter
	def tile_points(self,args):
		self.tile_x1,self.tile_y1,\
		self.tile_x2,self.tile_y2 = args

	#center
	@property
	def tile_center(self):
		return\
		self.tile_x+(self.tile_w/2),\
		self.tile_y+(self.tile_h/2)
	@tile_center.setter
	def tile_center(self,a):
		self.tile_x,self.tile_y = \
		a[0]-(self.tile_w/2), b[0]-(self.tile_h/2)



	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	#### ROOM

	#x
	@property
	def room_x(self): return int(self.x/RX)
	@room_x.setter
	def room_x(self,x): self.x = x*RX
	#
	#y
	@property
	def room_y(self): return int(self.y/RY)
	@room_y.setter
	def room_y(self,y): self.y = y*RY
	#
	#w
	@property
	def room_w(self): return int(self.w/RX)
	@room_w.setter
	def room_w(self,w): self.w = w*RX
	#
	#h
	@property
	def room_h(self): return int(self.h/RY)
	@room_h.setter
	def room_h(self,h): self.h = h*RY

	####

	#x1
	@property
	def room_x1(self): return self.room_x
	@room_x1.setter
	def room_x1(self, x1): self.room_x = x1
	#
	#y1
	@property
	def room_y1(self): return self.room_y
	@room_y1.setter
	def room_y1(self, y1): self.room_y = y1
	#
	#x2
	@property
	def room_x2(self):
		return self.room_x + self.room_w
	@room_x2.setter
	def room_x2(self, x2):
		self.room_x = x2 - self.room_w
	#
	#y2
	@property
	def room_y2(self):
		return self.room_y + self.room_h
	@room_y2.setter
	def room_y2(self, y2):
		self.room_y = y2 - self.room_h


	#position
	@property
	def room_position(self):
		return self.room_x, self.room_y
	@room_position.setter
	def room_position(self, args):
		self.room_x, self.room_y = args

	#size
	@property
	def room_size(self):
		return self.room_w, self.room_h
	@room_size.setter
	def room_size(self, args):
		self.room_w, self.room_h = args

	#points
	@property
	def room_points(self):
		return self.room_x1,self.room_y1,\
		self.room_x2,self.room_y2
	@room_points.setter
	def room_points(self,args):
		self.room_x1,self.room_y1,\
		self.room_x2,self.room_y2 = args

	#center
	@property
	def room_center(self):
		x,y = float(self.x)/RX,float(self.y)/RY
		w,h = float(self.w)/RX,float(self.h)/RY
		return int(x+(w/2)), int(y+(h/2))
	@room_center.setter
	def room_center(self,a):
		self.room_x,self.room_y = \
		a[0]-(self.room_w/2), a[1]-(self.room_h/2)


	###############################################

	def inside(self, R):
		a = self
		if type(R) == list or type(R) == tuple:
			b = Rectangle(); b.points = R
		else: b = R

		def x():
			if a.x1 < b.x1 < a.x2: return True
			if a.x1 < b.x2 < a.x2: return True
			if b.x1 < a.x1 < b.x2: return True
			if b.x1 < a.x2 < b.x2: return True
			return False

		def y():
			if a.y1 < b.y1 < a.y2: return True
			if a.y1 < b.y2 < a.y2: return True
			if b.y1 < a.y1 < b.y2: return True
			if b.y1 < a.y2 < b.y2: return True
			return False

		if x() and y(): return True
		return False


	def colliding(self, Rectangle):
		a = self
		if type(R) == list or type(R) == tuple:
			b = Rectangle(); b.points = R
		else: b = R

		def x():
			if a.x1 <= b.x1 <= a.x2: return True
			if a.x1 <= b.x2 <= a.x2: return True
			if b.x1 <= a.x1 <= b.x2: return True
			if b.x1 <= a.x2 <= b.x2: return True
			return False

		def y():
			if a.y1 <= b.y1 <= a.y2: return True
			if a.y1 <= b.y2 <= a.y2: return True
			if b.y1 <= a.y1 <= b.y2: return True
			if b.y1 <= a.y2 <= b.y2: return True
			return False

		if x() and y(): return True
		return False

	#

	def keep_in_points(self, pos=(), points=()):
		x,y = pos
		x1,y1,x2,y2 = points
		if x < x1: x = x1
		if x > x2: x = x2
		if y < y1: y = y1
		if y > y2: y = y2
		return x, y

	def in_points(self, pos=(), points=()):
		if pos == self.keep_in_points(pos, points):
			return True
		return False