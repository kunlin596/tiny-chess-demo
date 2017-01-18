import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication, QSurfaceFormat
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import qmlRegisterType

from model import ModelEntity, ModelEntityList
from scene_view import EditorView

if __name__ == '__main__':
	f = QSurfaceFormat()
	f.setVersion(4, 1)
	f.setProfile(QSurfaceFormat.CoreProfile)
	f.setDefaultFormat(f)

	app = QGuiApplication(sys.argv)

	qmlRegisterType(ModelEntity, 'MyEntity', 1, 0, 'Entity')
	qmlRegisterType(ModelEntityList, 'MyEntity', 1, 0, 'EntityList')

	view = EditorView()
	view.setResizeMode(QQuickView.SizeRootObjectToView)  # Set for the object to resize correctly
	view.setSource(QUrl('qml/ModelWindow.qml'))
	view.show()

	app.exec()
