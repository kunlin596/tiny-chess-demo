import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication, QOpenGLVersionProfile, QSurfaceFormat
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine

from scene_view import EditorView
import platform

if __name__ == '__main__':
	# Not working in Ubuntu 16.04, result in 1282 error for simple calling like glViewport(...)
	# TODO

	f = QSurfaceFormat()
	f.setVersion(4, 1)
	# f.setDepthBufferSize(1)  # fix depth buffer error
	# f.setStencilBufferSize(1)  # fix stencil buffer error
	f.setProfile(QSurfaceFormat.CoreProfile)
	# f.setOption(QSurfaceFormat.DebugContext)
	f.setDefaultFormat(f)

	app = QGuiApplication(sys.argv)

	view = EditorView()
	view.setResizeMode(QQuickView.SizeRootObjectToView)  # Set for the object to resize correctly
	view.setSource(QUrl('lib/ModelWindow.qml'))
	view.show()

	app.exec()
