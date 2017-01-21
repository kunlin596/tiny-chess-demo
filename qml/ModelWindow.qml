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

        onPressed: { click_pos = Qt.point(mouse.x,mouse.y); }

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
        gradient: static_color
        Gradient {
            id: static_color
            GradientStop { position: 0.0; color: Qt.rgba(0.15, 0.15, 0.15, 0.8)}
            GradientStop { position: 0.66; color: Qt.rgba(0.1, 0.1, 0.1, 0.8)}
            GradientStop { position: 1.0; color: Qt.rgba(0.1, 0.1, 0.1, 0.8)}
        }
        anchors {
            top: parent.top
            left: parent.left
        }
        Image {
            id: menu_image_shadow
            anchors.top: parent.top
            anchors.left: parent.right
            height: parent.height
            z: 4
            source: "shadow_long.png"
        }

        MyButton {
            id: edit_board_button
            text: 'Edit'
            property var show_menu: false

            ButtonWithMenu {
                id: change_color_button
                show_menu: false
                text: 'color'
                anchors {
                    top: parent.top
                    left: parent.right
                }

                slider {
                    text1: 'R'
                    text2: 'G'
                    text3: 'B'
                    value1: 0.0
                    value2: 0.0
                    value3: 0.0
                    min_val: 0.0
                    max_val: 1.0
                }
            }

            ButtonWithMenu {
                id: change_position_button
                show_menu: false
                text: 'translation'
                anchors {
                    top: change_color_button.bottom
                    left: parent.right
                }
                slider {
                    text1: 'X'
                    text2: 'Y'
                    text3: 'Z'
                    value1: 0.0
                    value2: 0.0
                    value3: 0.0
                    min_val: -50.0
                    max_val: 50.0
                }
            }

            ButtonWithMenu {
                id: change_rotation_button
                show_menu: false
                text: 'rotate'
                anchors {
                    top: change_position_button.bottom
                    left: parent.right
                }

                slider {
                    text1: 'Rx'
                    text2: 'Ry'
                    text3: 'Rz'
                    value1: 0.0
                    value2: 0.0
                    value3: 0.0
                    min_val: 0.0
                    max_val: 360.0
                }
            }

            ButtonWithMenu {
                id: change_scale_button
                show_menu: false
                text: 'scale'
                anchors {
                    top: change_rotation_button.bottom
                    left: parent.right
                }
                slider {
                    text1: 'X'
                    text2: 'Y'
                    text3: 'Z'
                    value1: 0.0
                    value2: 0.0
                    value3: 0.0
                    min_val: 10.0
                    max_val: 50.0
                }
            }

            MyButton {
                id: add_button
                text: "Add"
                state: "Invisible"
                anchors {
                    top: change_scale_button.bottom
                    left: parent.right
                }
            }

            MyButton {
                id: delete_button
                text: "Delete"
                state: "Invisible"
                anchors {
                    top: add_button.bottom
                    left: parent.right
                }

                mouse_area.onClicked: _window.on_delete_current_selection()
            }

            mouse_area {
                onClicked: {
                    if (edit_board_button.show_menu == false) {
                        change_color_button.state = "Visible"
                        change_position_button.state = "Visible"
                        change_rotation_button.state = "Visible"
                        change_scale_button.state = "Visible"
                        add_button.state = "Visible"
                        delete_button.state = "Visible"
                        edit_board_button.show_menu = true
                    }
                    else {
                        change_color_button.state = "Invisible"
                        change_position_button.state = "Invisible"
                        change_rotation_button.state = "Invisible"
                        change_scale_button.state = "Invisible"
                        add_button.state = "Invisible"
                        delete_button.state = "Invisible"
                        edit_board_button.show_menu = false
                    }
                }
            }

            Component.onCompleted: {
                change_color_button.slider.valueChanged.connect(_window.onColorChanged)
                change_position_button.slider.valueChanged.connect(_window.onPositionChanged)
                change_rotation_button.slider.valueChanged.connect(_window.onRotationChanged)
                change_scale_button.slider.valueChanged.connect(_window.onScaleChanged)

                _window.colorChanged.connect(change_color_button.onValueChanged)
                _window.positionChanged.connect(change_position_button.onValueChanged)
                _window.rotationChanged.connect(change_rotation_button.onValueChanged)
                _window.scaleChanged.connect(change_scale_button.onValueChanged)
            }
        }

        MyButton {
        id: reset_board_button
        anchors.top: edit_board_button.bottom
        text: 'Reset'
        mouse_area {
            onClicked: _window.reset_board()
        }
    }

        MyButton {
            id: list_button
            anchors.top: reset_board_button.bottom
            text: 'List'
            property bool show_menu: false
            ObjectList {
                id: object_list
                state: "Invisible"
                height: 400
                anchors {
                    top: parent.top
                    left: parent.right
                }
            }

            mouse_area {
                onClicked: {
                    if (list_button.show_menu == false) {
                        object_list.state = "Visible"
                        list_button.show_menu = true
                    } else {
                        object_list.state = "Invisible"
                        list_button.show_menu = false
                    }
                }
            }

        }
    }
}
