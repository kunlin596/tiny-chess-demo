import QtQuick 2.0
import QtGraphicalEffects 1.0

Rectangle {
    width: 100
    height: 50

    property alias text: text.text
    property alias mouse_area: mouse_area
    property color active_color:  Qt.rgba(0.0, 0.2, 0.8, 0.8)

    color: Qt.rgba(0.2, 0.2, 0.2, 0.8)
    Text {
        id: text
        text: 'Button'
        anchors.centerIn: parent
        font.pointSize: 10
        color: 'white'
    }

    Image {
        id: menu_image_shadow
        anchors.top: parent.top
        anchors.left: parent.right
        height: parent.height
        z: 4
        source: "shadow_long.png"
    }

    MouseArea {
        id: mouse_area

        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            parent.color = parent.active_color
        }

        onExited: {
            parent.color = Qt.rgba(0.2, 0.2, 0.2, 0.8)
        }

        onClicked: { }
    }

    Behavior on x {
       NumberAnimation{ duration: 300 }
    }

    Behavior on opacity {
       NumberAnimation{ duration: 300 }
    }
}