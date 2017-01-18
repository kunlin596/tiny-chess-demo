import numpy
import numpy as np
import pyassimp as ai
from PyQt5.Qt import QQmlListProperty
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import QVector3D
from PyQt5.QtQml import QQmlListProperty

from entity import CUBE_INDEX


class MeshData(object):
	"""
	Data structure for the mesh data
	"""

	def __init__ ( self,
	               name = 'None',
	               vertices = None,
	               colors = None,
	               normals = None,
	               indices = None,
	               texturecoords = None ):
		self.name = name
		self.vertices = vertices
		self.colors = colors
		self.normals = normals
		self.indices = indices
		self.texturecoords = texturecoords

	@classmethod
	def CheckData ( cls, mesh ):
		print(mesh.name + ':')
		if len(mesh.vertices) == 0:
			print(' vertices is empty')
		if len(mesh.colors) == 0:
			print(' colors is empty')
		if len(mesh.normals) == 0:
			print(' normals is empty')
		if len(mesh.indices) == 0:
			print(' indices is empty')
		if len(mesh.texturecoords) == 0:
			print(' texturecoords is empty')

	@classmethod
	def ReadFromFile ( cls, file_name, name = 'None' ):
		scene = ai.load(file_name)
		mesh = scene.meshes[0]
		vertices = mesh.vertices - 0.5
		indices = mesh.faces.flatten()  # make 1d for passing
		colors = mesh.colors
		normals = mesh.normals
		texturecoords = mesh.texturecoords
		return MeshData(name, vertices, colors, normals, indices, texturecoords)


class RawModel(object):
	def __init__ ( self, vao, indices_vbo, num_indices ):
		self.vao = vao
		self.indices_vbo = indices_vbo
		self.num_indices = num_indices  # For glDrawElements()


class ModelEntity(QQuickItem):
	def __init__ ( self, parent = None ):
		super(QQuickItem, self).__init__(parent)
		self._name = 'ModelEntity'
		self.model = None
		self.position = None
		self.rotation = None
		self.scale = None
		self.color = None

	@pyqtProperty('QString')
	def name ( self ):
		return '{0}'.format(self._name, self._name)

	@name.setter
	def name ( self, name ):
		self._name = name

	@pyqtProperty('QVector3D')
	def _position ( self ):
		return QVector3D(self.position[0], self.position[1], self.position[2])

	@_position.setter
	def _position ( self, vec ):
		self.position[0] = vec[0]
		self.position[1] = vec[1]
		self.position[2] = vec[2]

	@pyqtProperty('QVector3D')
	def _rotation ( self ):
		return QVector3D(self.rotation[0], self.rotation[1], self.rotation[2])

	@_rotation.setter
	def _rotation ( self, vec ):
		self.rotation[0] = vec[0]
		self.rotation[1] = vec[1]
		self.rotation[2] = vec[2]

	@pyqtProperty('QVector3D')
	def _scale ( self ):
		return QVector3D(self.scale[0], self.scale[1], self.scale[2])

	@_scale.setter
	def _scale ( self, vec ):
		self.scale[0] = vec[0]
		self.scale[1] = vec[1]
		self.scale[2] = vec[2]

	@pyqtProperty('QVector3D')
	def _color ( self ):
		return QVector3D(self.color[0], self.color[1], self.color[2])

	@_color.setter
	def _color ( self, vec ):
		self.color[0] = vec[0]
		self.color[1] = vec[1]
		self.color[2] = vec[2]


class ModelEntityList(QQuickItem):
	def __init__ ( self, parent = None ):
		super(QQuickItem, self).__init__(parent)
		self._entities = []

	@pyqtProperty(QQmlListProperty)
	def entities ( self ):
		"""
		This method is for Qml to access the list
		:return:
		"""
		return QQmlListProperty(ModelEntity, self, self._entities)

	@pyqtProperty(int)
	def length ( self ):
		return len(self._entities)

	def get_entities ( self ):
		"""
		This method is for Python to access the list
		:return:
		"""
		return self._entities

	def __getitem__ ( self, key ):
		if key >= len(self._entities):
			raise IndexError()
		return self._entities[key]

	def __setitem__ ( self, key, value ):
		self._entities[key] = value

	def __len__ ( self ):
		return len(self._entities)

	def append ( self, item ):
		self._entities.append(item)

	def extend ( self, lst ):
		self._entities.extend(lst)


class TexturedModel(object):
	def __init__ ( self, raw_model = None, texture = None ):
		self.raw_model = raw_model
		self.texture = texture


class Texture(object):
	def __init__ ( self, data = None, width = None, height = None ):
		self.data = data
		self.width = width
		self.height = height
		self.reflectivity = 0.0
		self.shine_damper = 1.0
		self.has_transparency = False

	@classmethod
	def CreateFromFile ( cls, file_name ):
		return Texture()


class EntityCreator(object):
	def __init__ ( self, models ):
		self._models = models

	def create_cube ( self, position, rotation, scale, color ):
		e = ModelEntity()
		e.model = self._models['cube']
		e.position = position
		e.rotation = rotation
		e.scale = scale
		e.color = color
		return e

	def create_bunny ( self, position, rotation, scale, color ):
		e = ModelEntity()
		e.model = self._models['bunny']
		e.position = position
		e.rotation = rotation
		e.scale = scale
		e.color = color
		return e

	def create_checker_board ( self, entities, length = 10.0, rows = 8, cols = 8 ):
		y = -0.25
		color_black = np.array([0.0, 0.0, 0.0])
		color_white = np.array([1.0, 1.0, 1.0])

		for row in range(rows):
			for col in range(cols):
				position = np.array([col * length - cols * length / 2.0 + length / 2.0,
				                     y,
				                     row * length - rows * length / 2.0 + length / 2.0])
				rotation = np.array([0.0, 0.0, 0.0])
				scale = np.array([9.0, 0.5, 9.0])
				if (col + row) % 2 == 0:
					color = color_black.copy()
				else:
					color = color_white.copy()

				e = ModelEntity()
				e.model = self._models[CUBE_INDEX]
				e.position = position
				e.rotation = rotation
				e.scale = scale
				e.color = color
				entities.append(e)
