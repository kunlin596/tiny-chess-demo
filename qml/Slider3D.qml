import QtQuick 2.0
import QtQuick.Controls 1.4

Rectangle {
	id: slider3d

    state: "Invisible"

    property alias label1: label1
    property alias label2: label2
    property alias label3: label3

    property alias slider1: val1
    property alias slider2: val2
    property alias slider3: val3

    width: 300
    height: 150

    gradient: static_color
    Gradient {
        id: static_color
        GradientStop { position: 0.0; color: Qt.rgba(0.2, 0.2, 0.2, 0.8)}
        GradientStop { position: 0.66; color: Qt.rgba(0.1, 0.1, 0.1, 0.8)}
        GradientStop { position: 1.0; color: Qt.rgba(0.1, 0.1, 0.1, 0.8)}
    }

    Label {
        id: label1
        text: 'val1'
        width: 100
        height: 50
        anchors.top: parent.top
        anchors.left: parent.left
        font.pointSize: 10
        color: 'white'
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }
    Slider {
        id:val1
        width: 180
        height: 50
        anchors.top: parent.top
        anchors.left: label1.right
        value: 0.5
    }

    Label {
        id: label2
        text: 'val2'
        width: 100
        height: 50
        font.pointSize: 10
        color: 'white'
        anchors.left: parent.left
        anchors.top: label1.bottom
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }
    Slider {
        id:val2
        width: 180
        height: 50
        anchors.top: val1.bottom
        anchors.left: label2.right
        value: 0.5
    }

    Label {
        id: label3
        text: 'val3'
        width: 100
        height: 50
        font.pointSize: 10
        color: 'white'
        anchors.left: parent.left
        anchors.top: label2.bottom
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }
    Slider {
        id:val3
        width: 180
        height: 50
        anchors.top: val2.bottom
        anchors.left: label3.right
        value: 0.5
    }

    Image {
        id: menu_image_shadow
        anchors.top: parent.top
        anchors.left: parent.right
        height: parent.height
        z: 4
        source: "shadow_long.png"
    }

    states: [
        State{
            name: "Visible"
            PropertyChanges{target: slider3d; opacity: 1.0}
            PropertyChanges{target: slider3d; visible: true}
        },
        State{
            name: "Invisible"
            PropertyChanges{target: slider3d; opacity: 0.0}
            PropertyChanges{target: slider3d; visible: false}
        }
    ]
    transitions: [
        Transition {
            from: "Visible"
            to: "Invisible"

            SequentialAnimation{
               NumberAnimation {
                   target: slider3d
                   property: "opacity"
                   duration: 200
                   easing.type: Easing.InOutQuad
               }
               NumberAnimation {
                   target: slider3d
                   property: "visible"
                   duration: 0
               }
            }
        },
        Transition {
            from: "Invisible"
            to: "Visible"
            SequentialAnimation{
               NumberAnimation {
                   target: slider3d
                   property: "visible"
                   duration: 0
               }
               NumberAnimation {
                   target: slider3d
                   property: "opacity"
                   duration: 200
                   easing.type: Easing.InOutQuad
               }
            }
        }
    ]
}