from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtCore import Qt
from PyQt5.QtQuick import QQuickView

from PyQt5.QtGui import QOpenGLShaderProgram, QOpenGLShader, QMatrix4x4, QOpenGLContext, QOpenGLDebugLogger
from utils import *

import random
import OpenGL.GL as GL
import numpy as np
import pyassimp as ai

FLOAT_SIZE = 4
DOUBLE_SIZE = 8
UNSIGNED_INT_SIZE = 4

CUBE_INDEX = 0
BUNNY_INDEX = 1


class EditorView(QQuickView):
	def __init__ (self, parent = None):
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

		self.setClearBeforeRendering(False)  # otherwise quick would clear everything we render

	def initialize_scene (self):
		self._renderer.initialize()
		self.resetOpenGLState()

	def render_scene (self):
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

	@pyqtSlot(float)
	def stretch_x (self, x):
		pass

	@pyqtSlot(float)
	def stretch_y (self, y):
		pass

	@pyqtSlot(float)
	def stretch_z (self, z):
		pass

	@pyqtSlot(int, int)
	def rotate_obj (self, x, y):
		pass

	@pyqtSlot(int, int)
	def rotate_camera (self, x, y):
		pass

	@pyqtSlot()
	def change_random_cube_color (self):
		self._renderer.change_random_cube_color()

	@pyqtSlot()
	def change_random_sphere_color (self):
		self._renderer.change_random_sphere_color()


class SceneRenderer(QObject):
	def __init__ (self, window = None, parent = None):
		super(SceneRenderer, self).__init__(parent)

		self._window = window
		self._camera = Camera()
		self._shader = None

		self._model_matrix = np.identity(4)
		self._projection_matrix = perspective_projection(45.0, 640.0 / 480.0, 0.001, 1000.0)

		self._cpu_manager = GpuManager()  # load data onto gpu
		self._mesh_data = dict()  # store all the raw mesh data
		self._models = dict()  # for model-entity look up
		self._entities = dict()

	def initialize (self):
		self.set_projection_matrix()
		self.set_viewport_size(self._window.size() * self._window.devicePixelRatio())
		self._mesh_data[CUBE_INDEX] = MeshData.ReadFromFile('mesh/cube.obj', 'cube')
		self._mesh_data[BUNNY_INDEX] = MeshData.ReadFromFile('mesh/bunny.obj', 'bunny')

		self.create_shader()
		# load all the mesh data into gpu
		self._shader.bind()
		for k, v in self._mesh_data.items():
			self._models[k] = self._cpu_manager.load_to_vao(v)
			self._entities[k] = []
		self._shader.release()

		for i in range(100):
			self.add_geometry(0)

	def sync (self):
		self.set_projection_matrix()

	def invalidate (self):
		# TODO
		pass

	def render (self):

		w = self._window.width() * 2
		h = self._window.height() * 2

		GL.glViewport(0, 0, w, h)
		GL.glClearColor(0.8, 0.8, 0.8, 1)
		GL.glEnable(GL.GL_DEPTH_TEST)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT)
		GL.glClear(GL.GL_DEPTH_BUFFER_BIT)

		view_matrix = self._camera.get_view_matrix()

		self._shader.bind()
		self._shader.setUniformValue('view_matrix',
		                             QMatrix4x4(view_matrix.flatten().tolist()))
		self._shader.setUniformValue('projection_matrix',
		                             QMatrix4x4(self._projection_matrix.flatten().tolist()).transposed())
		for k, v in self._entities.items():
			# create a transformation for every entity based on its pose
			self.setup_model(self._models[k])

			# [1] is paired for draw elements
			# [2] is draw simple array

			GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,
			                self._models[k].indices_vbo)  # [1] intel driver doesn't include this, must bind manually
			for entity in v:
				self.setup_entity(entity)
				GL.glDrawElements(GL.GL_TRIANGLES,
				                  self._models[k].num_indices,
				                  GL.GL_UNSIGNED_INT,
				                  None)  # [1]
			GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)  # [1]
			# GL.glDrawArrays(GL.GL_TRIANGLES,
			#                 0,
			#                 self._models[k].num_indices) # [2]
			self.release_model()

		self._shader.release()

		# Restore the OpenGL state for QtQuick rendering
		self._window.update()

	def set_viewport_size (self, size):
		self._viewport_size = size

	def set_projection_matrix (self):
		# Need to be set every time we change the size of the window
		self._projection_matrix = perspective_projection(45.0,
		                                                 self._window.width() / self._window.height(),
		                                                 0.001, 1000.0)

	def setup_model (self, model):
		raw_model = model
		GL.glBindVertexArray(raw_model.vao)
		GL.glEnableVertexAttribArray(0)
		GL.glEnableVertexAttribArray(1)

	# GL.glEnableVertexAttribArray(2)

	def release_model (self):
		GL.glDisableVertexAttribArray(0)
		GL.glDisableVertexAttribArray(1)
		# GL.glDisableVertexAttribArray(2)
		GL.glBindVertexArray(0)

	def setup_entity (self, entity):
		m = create_transformation_matrix(entity.position,
		                                 entity.rotation,
		                                 entity.scale)

		self._shader.setUniformValue('model_matrix', QMatrix4x4(m.flatten().tolist()))

	def add_geometry (self, geo_enum):
		if geo_enum == 0:
			self._entities[CUBE_INDEX].append(Entity(self._models[CUBE_INDEX],
			                                         np.array([random.uniform(-10.0, 10.0),
			                                                   random.uniform(-10.0, 10.0),
			                                                   random.uniform(-20.0, -10.0)]),
			                                         np.array([random.uniform(-45.0, 45.0),
			                                                   random.uniform(-45.0, 45.0),
			                                                   random.uniform(-45.0, 45.0)]),
			                                         np.array([1.0, 1.0, 1.0])))
		elif geo_enum == 1:
			self._entities[BUNNY_INDEX].append(Entity(self._models[BUNNY_INDEX],
			                                          np.array([random.uniform(-10.0, 10.0),
			                                                    random.uniform(-10.0, 10.0),
			                                                    random.uniform(-20.0, -10.0)]),
			                                          np.array([random.uniform(-30.0, 30.0),
			                                                    random.uniform(-30.0, 30.0),
			                                                    random.uniform(-30.0, 30.0)]),
			                                          np.array([10.0, 10.0, 10.0])))
		else:
			return

	def delete_geometry (self, geo_enum):
		pass

	def create_shader (self):
		self._shader = QOpenGLShaderProgram()
		self._shader.addShaderFromSourceFile(QOpenGLShader.Vertex, 'shaders/OpenGL_4_1/vertex.glsl')
		self._shader.addShaderFromSourceFile(QOpenGLShader.Fragment, 'shaders/OpenGL_4_1/fragment.glsl')
		self._shader.link()


class MeshData:
	"""
	Data structure for the mesh data
	"""

	def __init__ (self,
	              name = 'None',
	              vertices = None,
	              colors = None,
	              normals = None,
	              indices = None,
	              texturecoords = None):
		self.name = name
		self.vertices = vertices
		self.colors = colors
		self.normals = normals
		self.indices = indices
		self.texturecoords = texturecoords

	@classmethod
	def CheckData (cls, mesh):
		if len(mesh.vertices) == 0:
			print('vertices is empty')
		if len(mesh.colors) == 0:
			print('colors is empty')
		if len(mesh.normals) == 0:
			print('normals is empty')
		if len(mesh.indices) == 0:
			print('indices is empty')
		if len(mesh.texturecoords) == 0:
			print('texturecoords is empty')

	@classmethod
	def ReadFromFile (cls, file_name, name = 'None'):
		scene = ai.load(file_name)
		mesh = scene.meshes[0]
		vertices = mesh.vertices
		indices = mesh.faces.flatten()  # make 1d for passing
		colors = mesh.colors
		normals = mesh.normals
		texturecoords = mesh.texturecoords

		if len(colors) == 0:
			colors = np.array([[0.2, 0.2, 0.8] for i in range(len(vertices))])

		return MeshData(name, vertices, colors, normals, indices, texturecoords)


# Handler of vao and other thing related to gpu
class RawModel(object):
	def __init__ (self, vao, indices_vbo, num_indices):
		self.vao = vao
		self.indices_vbo = indices_vbo
		self.num_indices = num_indices  # For glDrawElements()


class Entity(object):
	def __init__ (self, model, position, rotation, scale):
		self.model = model
		self.position = position
		self.rotation = rotation
		self.scale = scale


# class TexturedModel(object):
# 	def __init__ ( self, raw_model = None, texture = None ):
# 		self.raw_model = raw_model
# 		self.texture = texture
#

# For loading mesh data into gpu
class GpuManager(object):
	POSITION_LOCATION = 0
	COLOR_LOCATION = 1
	NORMAL_LOCATION = 2

	def __init__ (self):
		self.vaos = []
		self.vbos = []
		self.textures = []

	def load_to_vao (self, mesh_data):
		"""
		Upload data to GPU
		:return: RawModel
		"""
		vao = self.create_and_bind_vao()
		self.set_vertex_attribute_data(GpuManager.POSITION_LOCATION, 3, mesh_data.vertices)
		self.set_vertex_attribute_data(GpuManager.COLOR_LOCATION, 3, mesh_data.colors)
		# self.set_vertex_attribute_data(GpuManager.NORMAL_LOCATION, 3, mesh_data.normals)

		indices_vbo = self.create_indices_buffer(mesh_data.indices)
		self.unbind_vao()

		return RawModel(vao, indices_vbo, len(mesh_data.indices))

	def set_vertex_attribute_data (self, attrib_id, component_size, data):
		data = data.astype(np.float32)  # data is of float64 by default
		vbo = GL.glGenBuffers(1)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
		GL.glBufferData(GL.GL_ARRAY_BUFFER, len(data) * FLOAT_SIZE * component_size, data, GL.GL_STATIC_DRAW)
		GL.glEnableVertexAttribArray(attrib_id)
		GL.glVertexAttribPointer(attrib_id, component_size, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
		self.vbos.append(vbo)

	# def load_texture ( self ):
	# 	texture = Texture.CreateFromFile('')
	# 	GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
	# 	GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
	# 	GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_LOD_BIAS, -0.4)

	def create_and_bind_vao (self):
		vao = GL.glGenVertexArrays(1)
		self.vaos.append(vao)
		GL.glBindVertexArray(vao)
		return vao

	def unbind_vao (self):
		GL.glBindVertexArray(0)

	def create_indices_buffer (self, indices):
		vbo = GL.glGenBuffers(1)
		GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vbo)
		GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,
		                len(indices) * UNSIGNED_INT_SIZE,
		                indices,
		                GL.GL_STATIC_DRAW)
		GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
		self.vbos.append(vbo)
		return vbo

	def release_all (self):
		for b in self.vaos:
			GL.glDeleteVertexArrays(b)
		for b in self.vbos:
			GL.glDeleteBuffers(b)


# class Texture(object):
# 	def __init__ ( self, data = None, width = None, height = None ):
# 		self.data = data
# 		self.width = width
# 		self.height = height
# 		self.reflectivity = 0.0
# 		self.shine_damper = 1.0
# 		self.has_transparency = False
#
# 	@classmethod
# 	def CreateFromFile ( cls, file_name ):
# 		return Texture()


class Camera(QObject):
	def __init__ (self, parent = None):
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

	def get_view_matrix (self):
		return self._m

	def get_projection_matrix (self):
		pass

	def update_view_matrix (self):
		self._m = look_at(self._eye, self._eye + self._target, self._up)

	@pyqtSlot(float)
	def move_horizontally (self, dist):
		self._eye += dist * normalize_vector(self.x)
		self._target += dist * normalize_vector(self.x)
		self.update_view_matrix()

	@pyqtSlot(float)
	def move_vertically (self, dist):
		self._eye += dist * normalize_vector(self.y)
		self._target += dist * normalize_vector(self.y)
		self.update_view_matrix()

	@pyqtSlot(float)
	def move_forward (self, dist):
		self._eye += dist * normalize_vector(self.z)
		self._target += dist * normalize_vector(self.z)
		self.update_view_matrix()

	@pyqtSlot()
	def rotate_horizontally (self, angle):
		pass

	@pyqtSlot()
	def rotate_vertically (self, angle):
		pass
