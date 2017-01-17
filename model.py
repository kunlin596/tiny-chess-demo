import numpy as np
import pyassimp as ai


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
	def ReadFromFile ( cls, file_name, name = 'None' ):
		scene = ai.load(file_name)
		mesh = scene.meshes[0]
		vertices = mesh.vertices - 0.5
		indices = mesh.faces.flatten()  # make 1d for passing
		colors = mesh.colors
		normals = mesh.normals
		texturecoords = mesh.texturecoords

		if len(colors) == 0:
			colors = np.array([[0.2, 0.2, 0.8] for i in range(len(vertices))])

		return MeshData(name, vertices, colors, normals, indices, texturecoords)


class RawModel(object):
	def __init__ ( self, vao, indices_vbo, num_indices ):
		self.vao = vao
		self.indices_vbo = indices_vbo
		self.num_indices = num_indices  # For glDrawElements()


class Entity(object):
	def __init__ ( self, model, position, rotation, scale, color ):
		self.model = model
		self.position = position
		self.rotation = rotation
		self.scale = scale
		self.color = color


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
