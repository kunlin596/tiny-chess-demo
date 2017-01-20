import QtQuick 2.0

Rectangle {
    id: my_button
    width: 100
    height: 50

    property alias text: text.text
    property alias mouse_area: mouse_area

    state: "Visible"

    gradient: static_color
    Gradient {
        id: static_color
        GradientStop { position: 0.0; color: Qt.rgba(0.15, 0.15, 0.15, 0.8)}
        GradientStop { position: 0.66; color: Qt.rgba(0.1, 0.1, 0.1, 0.8)}
        GradientStop { position: 1.0; color: Qt.rgba(0.1, 0.1, 0.1, 0.8)}
    }
    Gradient {
        id: active_color
        GradientStop { position: 0.0; color: Qt.rgba(0.5, 0.5, 0.7, 0.8)}
        GradientStop { position: 0.66; color: Qt.rgba(0.1, 0.1, 0.1, 0.8)}
        GradientStop { position: 1.0; color: Qt.rgba(0.0, 0.0, 0.0, 0.8)}
    }

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
            parent.gradient = active_color
        }

        onExited: {
            parent.gradient = static_color
        }

        onClicked: { }
    }

    states: [
        State{
            name: "Visible"
            PropertyChanges{target: my_button; opacity: 1.0}
            PropertyChanges{target: my_button; visible: true}
        },
        State{
            name: "Invisible"
            PropertyChanges{target: my_button; opacity: 0.0}
            PropertyChanges{target: my_button; visible: false}
        }
    ]
    transitions: [
        Transition {
            from: "Visible"
            to: "Invisible"

            SequentialAnimation{
               NumberAnimation {
                   target: my_button
                   property: "opacity"
                   duration: 200
                   easing.type: Easing.InOutQuad
               }
               NumberAnimation {
                   target: my_button
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
                   target: root
                   property: "visible"
                   duration: 0
               }
               NumberAnimation {
                   target: root
                   property: "opacity"
                   duration: 100
                   easing.type: Easing.InOutQuad
               }
            }
        }
    ]

}