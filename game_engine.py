from entity import *
from common import *
from PyQt5.QtCore import pyqtSignal


class BoardTable(object):
	def __init__ (self):
		super(BoardTable, self).__init__()
		self.selected = [None, None]
		self.table = [[TileInfo(TILE_EMPTY, None) for j in range(8)] for i in range(8)]

	def __getitem__ (self, item):
		return self.table[item]

	def __setitem__ (self, key, value):
		self.table[key] = value


class TileInfo(object):
	def __init__ (self, status, piece):
		self.status = status
		self.piece = piece


class PieceInfo(object):
	# TODO

	def __init__ (self, id, player, role):
		pass

	def test_legal_move (self, row, col):
		pass


class TestMove(object):
	# TODO

	@classmethod
	def TestMove (cls, role, current_pos, target_pos):
		if role == CHESS_KING_MODEL_INDEX:
			TestMove.KingMove(current_pos, target_pos)
		elif role == CHESS_QUEEN_MODEL_INDEX:
			pass
		elif role == CHESS_BISHOP_MODEL_INDEX:
			pass
		elif role == CHESS_KNIGHT_MODEL_INDEX:
			pass
		elif role == CHESS_TOWER_MODEL_INDEX:
			pass
		elif role == CHESS_PAWN_MODEL_INDEX:
			pass

	@classmethod
	def KingMove (cls, current_pos, target_pos):
		pass

	@classmethod
	def QueenMove (cls, current_pos, target_pos):
		pass

	@classmethod
	def BishopMove (cls, current_pos, target_pos):
		pass

	@classmethod
	def KnightMove (cls, current_pos, target_pos):
		pass

	@classmethod
	def TowerMove (cls, current_pos, target_pos):
		pass

	@classmethod
	def PawnMove (cls, current_pos, target_pos):
		pass


class GameEngine(QObject):
	delete_entity = pyqtSignal(int, int)

	"""
	This class is in charge of the whole logic in this program,
	It updates the table and manages the rules and then update renderer
	"""

	def __init__ (self, window, camera, parent = None):
		super(GameEngine, self).__init__(parent)
		self._window = window
		self._camera = camera
		self._hover_table = np.zeros(shape = (8, 8), dtype = np.int32)
		self._board_table = BoardTable()

		self._board_table[1][0].piece = BLACK_PAWN_8
		self._board_table[1][1].piece = BLACK_PAWN_7
		self._board_table[1][2].piece = BLACK_PAWN_6
		self._board_table[1][3].piece = BLACK_PAWN_5
		self._board_table[1][4].piece = BLACK_PAWN_4
		self._board_table[1][5].piece = BLACK_PAWN_3
		self._board_table[1][6].piece = BLACK_PAWN_2
		self._board_table[1][7].piece = BLACK_PAWN_1

		self._board_table[0][0].piece = BLACK_TOWER_2
		self._board_table[0][1].piece = BLACK_KNIGHT_2
		self._board_table[0][2].piece = BLACK_BISHOP_2
		self._board_table[0][3].piece = BLACK_KING
		self._board_table[0][4].piece = BLACK_QUEEN
		self._board_table[0][5].piece = BLACK_BISHOP_1
		self._board_table[0][6].piece = BLACK_KNIGHT_1
		self._board_table[0][7].piece = BLACK_TOWER_1

		self._board_table[6][0].piece = WHITE_PAWN_1
		self._board_table[6][1].piece = WHITE_PAWN_2
		self._board_table[6][2].piece = WHITE_PAWN_3
		self._board_table[6][3].piece = WHITE_PAWN_4
		self._board_table[6][4].piece = WHITE_PAWN_5
		self._board_table[6][5].piece = WHITE_PAWN_6
		self._board_table[6][6].piece = WHITE_PAWN_7
		self._board_table[6][7].piece = WHITE_PAWN_8

		self._board_table[7][0].piece = WHITE_TOWER_1
		self._board_table[7][1].piece = WHITE_KNIGHT_1
		self._board_table[7][2].piece = WHITE_BISHOP_1
		self._board_table[7][3].piece = WHITE_KING
		self._board_table[7][4].piece = WHITE_QUEEN
		self._board_table[7][5].piece = WHITE_BISHOP_2
		self._board_table[7][6].piece = WHITE_KNIGHT_2
		self._board_table[7][7].piece = WHITE_TOWER_2

		self._mouse_picker = MousePicker(self._camera)

		self._curr_row = -100
		self._curr_col = -100

		for i in range(8):
			self._board_table[0][i].status = TILE_OCCUPIED
			self._board_table[1][i].status = TILE_OCCUPIED
			self._board_table[6][i].status = TILE_OCCUPIED
			self._board_table[7][i].status = TILE_OCCUPIED

		self._has_selected = False
		self._selected_tile = [None, None]

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
		if button == 0 and self._board_table[self._curr_row][self._curr_col].status == TILE_OCCUPIED:
			if not self._has_selected:
				self._board_table[self._curr_row][self._curr_col].status = TILE_SELECTED
				self._board_table.selected = [self._curr_row, self._curr_col]
				self._has_selected = True
			else:
				self._board_table[self._selected_tile[0]][self._selected_tile[1]].status = TILE_OCCUPIED
				self._board_table[self._curr_row][self._curr_col].status = TILE_SELECTED
				self._board_table.selected = [self._curr_row, self._curr_col]
			self._selected_tile[0] = self._curr_row
			self._selected_tile[1] = self._curr_col

		elif self._has_selected and self._board_table[self._curr_row][self._curr_col].status == TILE_EMPTY:
			self._board_table[self._curr_row][self._curr_col].status = TILE_DESTINATION
			self._has_selected = False

		elif button == 1:
			if self._board_table[self._curr_row][self._curr_col].status == TILE_SELECTED:
				self._board_table[self._curr_row][self._curr_col].status = TILE_OCCUPIED
				self._has_selected = False
				self._board_table.selected = [None, None]

	def on_keyboard (self, key):
		pass

	def hover_table (self):
		return self._hover_table

	def board_table (self):
		return self._board_table

	def reset_board (self):
		self._hover_table = np.zeros(shape = (8, 8), dtype = np.int32)
		self._board_table = BoardTable()

		self._board_table[1][0].piece = BLACK_PAWN_8
		self._board_table[1][1].piece = BLACK_PAWN_7
		self._board_table[1][2].piece = BLACK_PAWN_6
		self._board_table[1][3].piece = BLACK_PAWN_5
		self._board_table[1][4].piece = BLACK_PAWN_4
		self._board_table[1][5].piece = BLACK_PAWN_3
		self._board_table[1][6].piece = BLACK_PAWN_2
		self._board_table[1][7].piece = BLACK_PAWN_1

		self._board_table[0][0].piece = BLACK_TOWER_2
		self._board_table[0][1].piece = BLACK_KNIGHT_2
		self._board_table[0][2].piece = BLACK_BISHOP_2
		self._board_table[0][3].piece = BLACK_KING
		self._board_table[0][4].piece = BLACK_QUEEN
		self._board_table[0][5].piece = BLACK_BISHOP_1
		self._board_table[0][6].piece = BLACK_KNIGHT_1
		self._board_table[0][7].piece = BLACK_TOWER_1

		self._board_table[6][0].piece = WHITE_PAWN_1
		self._board_table[6][1].piece = WHITE_PAWN_2
		self._board_table[6][2].piece = WHITE_PAWN_3
		self._board_table[6][3].piece = WHITE_PAWN_4
		self._board_table[6][4].piece = WHITE_PAWN_5
		self._board_table[6][5].piece = WHITE_PAWN_6
		self._board_table[6][6].piece = WHITE_PAWN_7
		self._board_table[6][7].piece = WHITE_PAWN_8

		self._board_table[7][0].piece = WHITE_TOWER_1
		self._board_table[7][1].piece = WHITE_KNIGHT_1
		self._board_table[7][2].piece = WHITE_BISHOP_1
		self._board_table[7][3].piece = WHITE_KING
		self._board_table[7][4].piece = WHITE_QUEEN
		self._board_table[7][5].piece = WHITE_BISHOP_2
		self._board_table[7][6].piece = WHITE_KNIGHT_2
		self._board_table[7][7].piece = WHITE_TOWER_2

		self._mouse_picker = MousePicker(self._camera)

		self._curr_row = -100
		self._curr_col = -100

		for i in range(8):
			self._board_table[0][i].status = TILE_OCCUPIED
			self._board_table[1][i].status = TILE_OCCUPIED
			self._board_table[6][i].status = TILE_OCCUPIED
			self._board_table[7][i].status = TILE_OCCUPIED

		self._has_selected = False
		self._selected_tile = [None, None]

	def delete_current_selection (self):
		if self._has_selected:
			self._has_selected = False
			self._board_table[self._selected_tile[0]][self._selected_tile[1]].status = TILE_EMPTY
			self._board_table.selected = [None, None]
			self.delete_entity.emit(self._selected_tile[0], self._selected_tile[1])
