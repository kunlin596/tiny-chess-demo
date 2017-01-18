import numpy as np
from entity import *


class GameEngine(object):
	"""
	This class is in charge of the whole logic in this program,
	It updates the table and manages the rules and then update renderer
	"""

	def __init__ ( self, window, camera ):
		self._window = window
		self._camera = camera
		self._hover_table = np.zeros(shape = (8, 8))
		self._piece_table = np.zeros(shape = (8, 8))
		self._mouse_picker = MousePicker(self._camera)

		self._curr_row = -100
		self._curr_col = -100

	def on_mouse_move ( self, x, y ):
		self._mouse_picker.update_ray(x, y, self._window.width(), self._window.height())
		plane_point = find_plane_point(self._camera.eye, self._camera.eye + self._mouse_picker.ray * 500.0)
		self._curr_row, self._curr_col = find_coords_on_plane(plane_point, 10.0, 8, 8)
		self._hover_table = np.zeros(shape = (8, 8))
		if self._curr_row is not None and self._curr_col is not None:
			for r in range(8):
				for c in range(8):
					self._hover_table[self._curr_row][self._curr_col] = 1.0

	def on_clicked ( self, button, x, y ):
		if button == 0:
			self._piece_table[self._curr_row][self._curr_col] += 1
		elif button == 1:
			if self._piece_table[self._curr_row][self._curr_col] == 0:
				pass
			else:
				self._piece_table[self._curr_row][self._curr_col] -= 1
				print(self._piece_table[self._curr_row][self._curr_col])

	def on_keyboard ( self, key ):
		pass

	def update_renderer ( self, renderer ):
		pass

	def board_table ( self ):
		return self._hover_table

	def piece_table ( self ):
		return self._piece_table
