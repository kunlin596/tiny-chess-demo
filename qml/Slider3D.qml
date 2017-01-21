import QtQuick 2.0
import QtQuick.Controls 1.4

Rectangle {
	id: slider3d
    state: "Invisible"

    property alias text1: label1.text
    property alias text2: label2.text
    property alias text3: label3.text

    property alias value1: val1.value
    property alias value2: val2.value
    property alias value3: val3.value

    property real max_val: 1.0
    property real min_val: 0.0

    signal valueChanged(real val1, real val2, real val3)

    width: 340
    height: 150

    gradient: static_color
    Gradient {
        id: static_color
        GradientStop { position: 0.0; color: Qt.rgba(0.2, 0.2, 0.2, 0.8)}
        GradientStop { position: 0.66; color: Qt.rgba(0.1, 0.1, 0.1, 0.8)}
        GradientStop { position: 1.0; color: Qt.rgba(0.1, 0.1, 0.1, 0.8)}
    }

    // Slider 1
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
    Label {
        id: min_val_label1
        text: min_val
        width: 20
        height: 50
        anchors.top: parent.top
        anchors.left: label1.right
        font.pointSize: 10
        color: 'white'
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }
    Label {
        id: max_val_label1
        text: max_val
        width: 20
        height: 50
        anchors.top: parent.top
        anchors.left: val1.right
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
        anchors.left: min_val_label1.right
        value: 0.5
        minimumValue: slider3d.min_val
        maximumValue: slider3d.max_val
    }


    // Slider 2
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
    Label {
        id: min_val_label2
        text: min_val
        width: 20
        height: 50
        anchors.top: min_val_label1.bottom
        anchors.left: label2.right
        font.pointSize: 10
        color: 'white'
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }
    Label {
        id: max_val_label2
        text: max_val
        width: 20
        height: 50
        anchors.top: max_val_label1.bottom
        anchors.left: val2.right
        font.pointSize: 10
        color: 'white'
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }

    Slider {
        id:val2
        width: 180
        height: 50
        anchors.top: val1.bottom
        anchors.left: min_val_label2.right
        value: 0.5
        minimumValue: slider3d.min_val
        maximumValue: slider3d.max_val
    }

    // Slider 3
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
    Label {
        id: min_val_label3
        text: min_val
        width: 20
        height: 50
        anchors.top: min_val_label2.bottom
        anchors.left: label3.right
        font.pointSize: 10
        color: 'white'
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }
    Label {
        id: max_val_label3
        text: max_val
        width: 20
        height: 50
        anchors.top: max_val_label2.bottom
        anchors.left: val3.right
        font.pointSize: 10
        color: 'white'
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }

    Slider {
        id:val3
        width: 180
        height: 50
        anchors.top: val2.bottom
        anchors.left: min_val_label3.right
        value: 0.5
        minimumValue: slider3d.min_val
        maximumValue: slider3d.max_val
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

    Component.onCompleted: {
        val1.valueChanged.connect(slider3d.sendValueChangedSignal)
        val2.valueChanged.connect(slider3d.sendValueChangedSignal)
        val3.valueChanged.connect(slider3d.sendValueChangedSignal)
    }

    function sendValueChangedSignal() {
        slider3d.valueChanged(val1.value, val2.value, val3.value)
    }
}