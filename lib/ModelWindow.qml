import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.0

Item {

    id: root
    width: 640
    height: 480
    property variant click_pos: "0,0"


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

        hoverEnabled: true

        onPressed: {
            click_pos = Qt.point(mouse.x,mouse.y)
        }

        onClicked: {
            _window.set_mouse_position(mouse.x, mouse.x)
        }

        onPositionChanged: {
            if (pressed) {
                var delta = Qt.point(mouse.x - click_pos.x, mouse.y - click_pos.y);
                _window.rotate_camera(delta.x, delta.y);
            }
            _window.set_mouse_position(mouse.x, mouse.x)
        }

    }


//    Rectangle {
//        id: rectangle
//        width: 200
//        color: "#804b2e83"
//        radius: 0
//        border.width: 0
//        anchors.left: parent.left
//        anchors.leftMargin: 0
//        anchors.bottom: parent.bottom
//        anchors.bottomMargin: 0
//        anchors.top: parent.top
//        anchors.topMargin: 0
//        z: -1
//
//        ColumnLayout {
//            id: columnLayout1
//            spacing: 10
//            anchors.rightMargin: 8
//            anchors.bottomMargin: 8
//            anchors.leftMargin: 8
//            anchors.topMargin: 8
//            anchors.fill: parent
//
//            ColumnLayout {
//                id: columnLayout2
//                width: 100
//                height: 100
//                Layout.minimumWidth: 100
//
//                Button {
//                    id: button
//                    width: 110
//                    height: 22
//                    text: qsTr("Add Cube")
//                    Layout.fillWidth: true
//                }
//
//                Button {
//                    id: button3
//                    width: 110
//                    height: 22
//                    text: qsTr("Add Bunny")
//                    Layout.fillWidth: true
//                }
//            }
//
//            ColumnLayout {
//                id: columnLayout
//                width: 100
//                height: 100
//
//                Label {
//                    id: label3
//                    text: qsTr("Model List")
//                }
//
//                ListView {
//                    id: listView
//                    width: 110
//                    height: 169
//                    spacing: 2
//                    Layout.minimumWidth: 100
//                    Layout.fillWidth: true
//                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                    layoutDirection: Qt.LeftToRight
//                    boundsBehavior: Flickable.DragOverBounds
//                    interactive: true
//                    delegate: Item {
//                        x: 5
//                        width: 80
//                        height: 40
//                        Row {
//                            id: row1
//                            Rectangle {
//                                width: 40
//                                height: 40
//                                color: colorCode
//                            }
//
//                            Text {
//                                text: name
//                                font.bold: true
//                                anchors.verticalCenter: parent.verticalCenter
//                            }
//                            spacing: 10
//                        }
//                    }
//                    model: ListModel {
//                        //                    ListElement {
//                        //                        name: "Grey"
//                        //                        colorCode: "grey"
//                        //                    }
//                        //
//                        //                    ListElement {
//                        //                        name: "Red"
//                        //                        colorCode: "red"
//                        //                    }
//                        //
//                        //                    ListElement {
//                        //                        name: "Blue"
//                        //                        colorCode: "blue"
//                        //                    }
//                        //
//                        //                    ListElement {
//                        //                        name: "Green"
//                        //                        colorCode: "green"
//                        //                    }
//                    }
//                }
//
//            }
//
//            Button {
//                id: deleteButton
//                width: 110
//                height: 22
//                text: qsTr("Delete")
//                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//            }
//
//            GroupBox {
//                id: groupBox
//                Layout.minimumWidth: 100
//                visible: true
//                Layout.fillWidth: true
//                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                title: qsTr("Change Color")
//
//                GridLayout {
//                    id: gridLayout
//                    anchors.rightMargin: 5
//                    anchors.leftMargin: 5
//                    anchors.bottomMargin: 5
//                    anchors.topMargin: 5
//                    anchors.fill: parent
//                    rows: 3
//                    columns: 2
//
//                    Label {
//                        id: label
//                        text: qsTr("R")
//                        verticalAlignment: Text.AlignVCenter
//                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                    }
//
//                    TextEdit {
//                        id: textEdit
//                        width: 80
//                        height: 20
//                        text: qsTr("1.0")
//                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                        font.pixelSize: 12
//                    }
//
//                    Label {
//                        id: label1
//                        text: qsTr("G")
//                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                    }
//
//                    TextEdit {
//                        id: textEdit1
//                        width: 80
//                        height: 20
//                        text: qsTr("1.0")
//                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                        font.pixelSize: 12
//                    }
//
//                    Label {
//                        id: label2
//                        text: qsTr("B")
//                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                    }
//
//
//                    TextEdit {
//                        id: textEdit2
//                        width: 80
//                        height: 20
//                        text: qsTr("1.0")
//                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                        font.pixelSize: 12
//                    }
//
//                    Button {
//                        id: button2
//                        text: qsTr("Enter")
//                    }
//
//                    Button {
//                        id: button1
//                        text: qsTr("Reset")
//                    }
//
//
//
//
//
//
//
//
//
//
//
//                }
//            }
//
//
//        }
//
//
//
//
//
//
//
//
//
//
//    }

}
