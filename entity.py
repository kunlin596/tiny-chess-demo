from utils import *


class Camera(QObject):
	def __init__ ( self, parent = None ):
		super(Camera, self).__init__(parent)
		self._eye = np.array([0.0, 0.0, -30.0])
		self._up = np.array([0.0, 1.0, 0.0])
		self._target = np.array([0.0, 0.0, 1.0])
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
		self._m = look_at(self._eye, self._eye + self._target, self._up)

	@pyqtSlot(float)
	def move_horizontally ( self, dist ):
		self._eye += dist * normalize_vector(self.x)
		self._target += dist * normalize_vector(self.x)
		self.update_view_matrix()

	@pyqtSlot(float)
	def move_vertically ( self, dist ):
		self._eye += dist * normalize_vector(self.y)
		self._target += dist * normalize_vector(self.y)
		self.update_view_matrix()

	@pyqtSlot(float)
	def move_forward ( self, dist ):
		self._eye += dist * normalize_vector(self.z)
		self._target += dist * normalize_vector(self.z)
		self.update_view_matrix()

	@pyqtSlot()
	def rotate_horizontally ( self, angle ):
		pass

	@pyqtSlot()
	def rotate_vertically ( self, angle ):
		pass


class Light(object):
	def __init__ ( self, name, position, color ):
		self.name = name
		self.position = position
		self.color = color
