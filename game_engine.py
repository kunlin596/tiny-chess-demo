import numpy as np


class GameEngine(object):
	"""
	This class is in charge of the whole logic in this program,
	It updates the table and manages the rules and then update renderer
	"""

	def __init__ ( self ):
		self._checker_board_table = np.zeros(shape = (8, 8))

	def on_mouse ( self ):
		pass

	def on_keyboard ( self ):
		pass

	def update_renderer ( self, renderer ):
		pass
