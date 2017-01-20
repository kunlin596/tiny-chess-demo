from PyQt5.QtCore import Qt
from PyQt5.QtQuick import QQuickView

from entity import *
from render_engine import SceneRenderer
from game_engine import GameEngine


class EditorView(QQuickView):
	def __init__ (self, parent = None):
		super(EditorView, self).__init__(parent)
		self._renderer = None
		self._camera = Camera()
		self._renderer = SceneRenderer(self, self._camera)
		self._game = GameEngine(self, self._camera)

		self.sceneGraphInitialized.connect(self.initialize_scene, type = Qt.DirectConnection)
		self.beforeSynchronizing.connect(self.synchronize_scene, type = Qt.DirectConnection)
		self.beforeRendering.connect(self.render_scene, type = Qt.DirectConnection)
		self.sceneGraphInvalidated.connect(self.invalidate_scene, type = Qt.DirectConnection)

		self.rootContext().setContextProperty("_camera", self._camera)
		self.rootContext().setContextProperty("_window", self)
		# self.rootContext().setContextProperty("_checker_board_entities", self._renderer._title_entities)

		self.setClearBeforeRendering(False)  # otherwise quick would clear everything we render

	def initialize_scene (self):
		self._renderer.initialize()
		self.resetOpenGLState()

	def render_scene (self):
		self._renderer.prepare_hover_table(self._game.hover_table())
		self._renderer.prepare_board_table(self._game.board_table())
		self._renderer.render()
		self.resetOpenGLState()

	def invalidate_scene (self):
		self._renderer.invalidate()
		self.resetOpenGLState()

	def synchronize_scene (self):
		self._renderer.sync()
		self.resetOpenGLState()

	@pyqtSlot(int)
	def add_geometry (self, geo_enum):
		self._renderer.add_geometry(geo_enum)

	@pyqtSlot(int)
	def delete_geometry (self, index):
		self._renderer.delete_geometry(index)

	@pyqtSlot(int)
	def select_obj (self, index = 0):
		pass

	@pyqtSlot(int, int)
	def rotate_camera (self, dx, dy):
		self._renderer.rotate_camera(dx, dy)

	@pyqtSlot(int)
	def move_camera (self, key):
		self._renderer.move_camera(key)

	@pyqtSlot(int, int)
	def set_mouse_position (self, x, y):
		self._renderer.update_mouse_position(x, y)

	@pyqtSlot(int, int)
	def on_hover (self, x, y):
		self._game.on_mouse_move(x, y)

	@pyqtSlot(int, int, int)
	def on_clicked (self, button, x, y):
		self._game.on_clicked(button, x, y)
