from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtQuick import QQuickView

from entity import Camera
from render_engine import SceneRenderer

from model import ModelEntity, ModelEntityList


class EditorView(QQuickView):
	def __init__ ( self, parent = None ):
		super(EditorView, self).__init__(parent)
		self._renderer = None
		self._camera = Camera()
		self._renderer = SceneRenderer(self)

		self.sceneGraphInitialized.connect(self.initialize_scene, type = Qt.DirectConnection)
		self.beforeSynchronizing.connect(self.synchronize_scene, type = Qt.DirectConnection)
		self.beforeRendering.connect(self.render_scene, type = Qt.DirectConnection)
		self.sceneGraphInvalidated.connect(self.invalidate_scene, type = Qt.DirectConnection)

		self.rootContext().setContextProperty("_camera", self._camera)
		self.rootContext().setContextProperty("_window", self)
		self.rootContext().setContextProperty("_checker_board_entities", self._renderer._checker_board_entities)

		self.setClearBeforeRendering(False)  # otherwise quick would clear everything we render

	def initialize_scene ( self ):
		self._renderer.initialize()
		self.resetOpenGLState()

	def render_scene ( self ):
		self._renderer.render()
		self.resetOpenGLState()

	def invalidate_scene ( self ):
		self._renderer.invalidate()
		self.resetOpenGLState()

	def synchronize_scene ( self ):
		self._renderer.sync()
		self.resetOpenGLState()

	@pyqtSlot(int)
	def add_geometry ( self, geo_enum ):
		self._renderer.add_geometry(geo_enum)

	@pyqtSlot(int)
	def delete_geometry ( self, index ):
		self._renderer.delete_geometry(index)

	@pyqtSlot(int)
	def select_obj ( self, index = 0 ):
		pass

	@pyqtSlot(int, int)
	def rotate_camera ( self, dx, dy ):
		self._renderer.rotate_camera(dx, dy)

	@pyqtSlot(int)
	def move_camera ( self, key ):
		self._renderer.move_camera(key)

	@pyqtSlot(int, int)
	def set_mouse_position ( self, x, y ):
		self._renderer.update_mouse_position(x, y)

	@pyqtSlot(int, int)
	def on_clicked ( self, x, y ):
		pass
