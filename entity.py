import numpy

from model import Entity
from utils import *
from enum import Enum

CUBE_INDEX = 0
BUNNY_INDEX = 1


class Camera(QObject):
	class Translation:
		LEFT = 0
		RIGHT = 1
		UP = 2
		DOWN = 3
		FORWARD = 4
		BACKWARD = 5

	class Rotation:
		Vertical = 0
		Horizontal = 1

	def __init__ ( self, parent = None ):
		super(Camera, self).__init__(parent)
		self.eye = np.array([0.0, 40.0, -20.0])
		self.up = np.array([0.0, 1.0, 0.0])
		self.target = np.array([0.0, -0.2, 0.8])
		self.x = None
		self.y = None
		self.z = None

		self.mouse_x = 0.0
		self.mouse_y = 0.0
		self._m = np.identity(4)
		self.update_view_matrix()

	def get_view_matrix ( self ):
		return self._m

	def get_projection_matrix ( self ):
		pass

	def update_view_matrix ( self ):
		self._m = look_at(self.eye, self.eye + self.target, self.up)

	@pyqtSlot(float)
	def translate ( self, dist ):
		self.eye += dist * normalize_vector(self.x)
		self.target += dist * normalize_vector(self.x)
		self.update_view_matrix()

	@pyqtSlot(float)
	def rotate ( self, dist ):
		self.eye += dist * normalize_vector(self.y)
		self.target += dist * normalize_vector(self.y)
		self.update_view_matrix()


class Light(object):
	def __init__ ( self, name, position, color ):
		self.name = name
		self.position = position
		self.color = color


class EntityCreator(object):
	def __init__ ( self, models ):
		self._models = models

	def create_cube ( self, position, rotation, scale, color ):
		return Entity(self._models['cube'],
		              position,
		              rotation,
		              scale,
		              color)

	def create_bunny ( self, position, rotation, scale, color ):
		return Entity(self._models['bunny'],
		              position,
		              rotation,
		              scale,
		              color)

	def create_checker_board ( self, length = 10.0, rows = 10, cols = 10 ):
		entities = []

		y = -0.2
		width = length
		height = length

		color_black = np.array([0.0, 0.0, 0.0])
		color_white = np.array([1.0, 1.0, 1.0])

		for row in range(rows):
			for col in range(cols):
				position = np.array([col * 10.0 - cols * 10.0 / 2 + 5.0, y, row * 10.0 + 10.0 * rows / 2 - 5.0])
				rotation = np.array([0.0, 0.0, 0.0])
				scale = np.array([10.0, 0.2, 10.0])
				if (col + row) % 2 == 0:
					color = color_black
				else:
					color = color_white
				entities.append(Entity(self._models[CUBE_INDEX],
				                       position,
				                       rotation,
				                       scale,
				                       color))

		return entities
