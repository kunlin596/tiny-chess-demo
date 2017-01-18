from utils import *

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
		self.eye = np.array([-60.0, 40.0, -60.0])
		self.up = np.array([0.0, 1.0, 0.0])
		self.target = np.array([0.6, -0.4, 0.6])
		self.x = None
		self.y = None
		self.z = None

		self.mouse_x = 0.0
		self.mouse_y = 0.0
		self._view_matrix = np.identity(4)
		self._projection_matrix = np.identity(4)
		self.update_view_matrix()

	def get_view_matrix ( self ):
		return self._view_matrix

	def get_projection_matrix ( self ):
		return self._projection_matrix

	def update_view_matrix ( self ):
		self._view_matrix = look_at(self.eye, self.eye + self.target, self.up)

	def update_projection_matrix ( self, w, h ):
		self._projection_matrix = perspective_projection(45.0, w / h, 0.001, 500.0)

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
