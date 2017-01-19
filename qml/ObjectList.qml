import QtQuick 2.0


Rectangle {
    x: 0
    width: 100;
    color: Qt.rgba(0.2, 0.2, 0.2, 0.7)

    ListView {
        id: listView
        width: 100
        anchors.fill:parent
        clip: true

        model: listModel
        delegate: Button {
            text: hour
        }
    }

    Image {
        id: menu_image_shadow
        anchors.top: parent.top
        anchors.left: parent.right
        height: parent.height
        z: 4
        source: "shadow_long.png"
    }

    Behavior on opacity {
        NumberAnimation {
            duration: 300
        }
    }

    Behavior on x {
        NumberAnimation {
            duration: 300
        }
    }

    ListModel {
        id: listModel
        Component.onCompleted: {
            for (var i = 0; i < 10; i++) {
                append(createListElement(i));
            }
        }
        function createListElement(i) {
            return {
                hour: i
            };
        }
    }
}