import unittest

from render_engine import MeshData


class MeshDataLoaderTest(unittest.TestCase):
	def test_loading ( self ):
		mesh = MeshData.ReadFromFile('../mesh/cube.obj')
		self.assertTrue(mesh.vertices is not None)
		self.assertTrue(mesh.colors is not None)
		self.assertTrue(mesh.normals is not None)
		self.assertTrue(mesh.indices is not None)
		self.assertTrue(mesh.texturecoords is not None)

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
