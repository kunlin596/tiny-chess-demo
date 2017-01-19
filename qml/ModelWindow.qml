import QtQuick 2.0
import QtQuick.Layouts 1.0
//import MyEntity 1.0
import "componentCreation.js" as EntityCreationHelper

Item {

    id: root
    width: 640
    height: 480
    property variant click_pos: "0, 0"

    focus: true


    Keys.onPressed: {
        switch(event.key) {
            case Qt.Key_W:
                _window.move_camera(4);
                break;
            case Qt.Key_S:
                _window.move_camera(5);
                break;
            case Qt.Key_A:
                _window.move_camera(0);
                break;
            case Qt.Key_D:
                _window.move_camera(1);
                break;
            case Qt.Key_Space:
            case Qt.Key_O:
                _window.move_camera(2);
                break;
            case Qt.Key_P:
                _window.move_camera(3);
                break;
        }
    }

    MouseArea {
        anchors.fill: parent

        acceptedButtons: Qt.LeftButton | Qt.RightButton

        hoverEnabled: true

        onPressed: {
            click_pos = Qt.point(mouse.x,mouse.y);
        }

        onClicked: {
            if (mouse.button == Qt.LeftButton) {
                _window.on_clicked(0, mouse.x, mouse.y);
            } else if (mouse.button == Qt.RightButton) {
                _window.on_clicked(1, mouse.x, mouse.y);
            }
            _window.set_mouse_position(mouse.x, mouse.y);
        }

        onPositionChanged: {
            if (pressed) {
                var delta = Qt.point(mouse.x - click_pos.x, mouse.y - click_pos.y);
                _window.rotate_camera(delta.x, delta.y);
                // Disable mouse picking for
                _window.set_mouse_position(-100.0, -100.0);
            } else {
                _window.on_hover(mouse.x, mouse.y);
                _window.set_mouse_position(mouse.x, mouse.y);
            }
            mouse.accepted = false;
        }
    }

    Rectangle {
        id : control_panel
        width: 100.0
        height: parent.height
        anchors {
            top: parent.top
            left: parent.left
        }
        color: Qt.rgba(0.2, 0.2, 0.2, 0.7)
        Image {
            id: menu_image_shadow
            anchors.top: parent.top
            anchors.left: parent.right
            height: parent.height
            z: 4
            source: "shadow_long.png"
        }

//        MouseArea {
//            anchors.fill: parent
//            hoverEnabled: true
//            onEntered: {
//                parent.color = Qt.rgba(0.5, 0.5, 0.5, 0.7)
//            }
//            onExited: {
//                parent.color = Qt.rgba(0.2, 0.2, 0.2, 0.7)
//            }
//        }
    }

    Button {
        id: button1
        text: 'Edit'
        Button {
            id: change_color_button
            text: 'Color'
            opacity: 0.0
            x: -100
            active_color: Qt.rgba(0.9, 0.2, 0.0, 0.8)
            anchors {
                top: parent.top
            }
        }
        Button {
            id: change_position_button
            text: 'Translate'
            opacity: 0.0
            x: -100
            active_color: Qt.rgba(0.9, 0.2, 0.0, 0.8)
            anchors {
                top: change_color_button.bottom
            }
        }
        Button {
            id: change_orientation_button
            text: 'Rotate'
            opacity: 0.0
            x: -100
            active_color: Qt.rgba(0.9, 0.2, 0.0, 0.8)
            anchors {
                top: change_position_button.bottom
            }
        }
        Button {
            id: change_scale_button
            text: 'Scale'
            opacity: 0.0
            x: -100
            active_color: Qt.rgba(0.9, 0.2, 0.0, 0.8)
            anchors {
                top: change_orientation_button.bottom
            }
        }
        Button {
            id: add_button
            text: 'Add'
            opacity: 0.0
            x: -100
            active_color: Qt.rgba(0.9, 0.2, 0.0, 0.8)
            anchors {
                top: change_scale_button.bottom
            }
        }
        Button {
            id: delete_button
            text: 'Delete'
            opacity: 0.0
            x: -100
            active_color: Qt.rgba(0.9, 0.2, 0.0, 0.8)
            anchors {
                top: add_button.bottom
            }
        }
        mouse_area {
            onClicked: {
                if (change_color_button.opacity == 0.0) {
                    change_color_button.opacity = 1.0
                    change_position_button.opacity = 1.0
                    change_orientation_button.opacity = 1.0
                    change_scale_button.opacity = 1.0
                    add_button.opacity = 1.0
                    delete_button.opacity = 1.0

                    change_color_button.x = 100
                    change_position_button.x = 100
                    change_orientation_button.x = 100
                    change_scale_button.x = 100
                    add_button.x = 100
                    delete_button.x = 100

                } else {
                    change_color_button.opacity = 0.0
                    change_position_button.opacity = 0.0
                    change_orientation_button.opacity = 0.0
                    change_scale_button.opacity = 0.0
                    add_button.opacity = 0.0
                    delete_button.opacity = 0.0

                    change_color_button.x = -100
                    change_position_button.x = -100
                    change_orientation_button.x = -100
                    change_scale_button.x = -100
                    add_button.x = -100
                    delete_button.x = -100
                }
            }
        }
    }

    Button {
        id: button2
        anchors.top: button1.bottom
        text: 'Reset'
    }

    Button {
        id: list_button
        anchors.top: button2.bottom
        text: 'List'
        mouse_area {
            onClicked: {
                if (object_list.opacity == 1.0) {
                    object_list.x = -100
                    object_list.opacity = 0.0
                } else {
                    object_list.x = 100
                    object_list.opacity = 1.0
                }
            }
        }
        ObjectList {
            id: object_list
            height: root.height
            opacity: 0.0
            x: -100
        }
    }

}
