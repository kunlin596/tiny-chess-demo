from entity import *
from common import *


class GameEngine(object):
	"""
	This class is in charge of the whole logic in this program,
	It updates the table and manages the rules and then update renderer
	"""

	def __init__ (self, window, camera):
		self._window = window
		self._camera = camera
		self._hover_table = np.zeros(shape = (8, 8))
		self._piece_table = np.zeros(shape = (8, 8), dtype = np.int32)
		self._mouse_picker = MousePicker(self._camera)

		self._curr_row = -100
		self._curr_col = -100

		for i in range(8):
			self._piece_table[0][i] = TILE_OCCUPIED
			self._piece_table[1][i] = TILE_OCCUPIED
			self._piece_table[6][i] = TILE_OCCUPIED
			self._piece_table[7][i] = TILE_OCCUPIED

		self._has_selected = False
		self._selected_tile = [None, None]
		self._moved = False

	def on_mouse_move (self, x, y):
		self._mouse_picker.update_ray(x, y, self._window.width(), self._window.height())
		plane_point = find_plane_point(self._camera.eye, self._camera.eye + self._mouse_picker.ray * 500.0)
		self._curr_row, self._curr_col = find_coords_on_plane(plane_point, 10.0, 8, 8)
		self._hover_table = np.zeros(shape = (8, 8))
		if self._curr_row is not None and self._curr_col is not None:
			for r in range(8):
				for c in range(8):
					self._hover_table[self._curr_row][self._curr_col] = 1

	def on_clicked (self, button, x, y):
		self._mouse_picker.update_ray(x, y, self._window.width(), self._window.height())
		plane_point = find_plane_point(self._camera.eye, self._camera.eye + self._mouse_picker.ray * 500.0)
		self._curr_row, self._curr_col = find_coords_on_plane(plane_point, 10.0, 8, 8)
		if self._curr_row is None or self._curr_col is None:
			return
		if button == 0 and self._piece_table[self._curr_row][self._curr_col] == TILE_OCCUPIED:
			if not self._has_selected:
				self._piece_table[self._curr_row][self._curr_col] = TILE_SELECTED
				self._has_selected = True
			else:
				self._piece_table[self._selected_tile[0]][self._selected_tile[1]] = TILE_OCCUPIED
				self._piece_table[self._curr_row][self._curr_col] = TILE_SELECTED
			self._selected_tile[0] = self._curr_row
			self._selected_tile[1] = self._curr_col

		elif self._has_selected and self._piece_table[self._curr_row][self._curr_col] == TILE_EMPTY:
			self._piece_table[self._curr_row][self._curr_col] = TILE_DESTINATION
			self._has_selected = False

		elif button == 1:
			if self._piece_table[self._curr_row][self._curr_col] == TILE_SELECTED:
				self._piece_table[self._curr_row][self._curr_col] = TILE_OCCUPIED
				self._has_selected = False

	def on_keyboard (self, key):
		pass

	def update_renderer (self, renderer):
		pass

	def board_table (self):
		return self._hover_table

	def piece_table (self):
		return self._piece_table
