MyButton {
    id: root
    property bool show_menu: false
    state: "Invisible"
    text: 'Button'

    Slider3D {
        id: slider
        state: "Invisible"
        anchors.top: parent.top
        anchors.left: parent.right
        label1 {
            text: 'label1'
        }
        label2 {
            text: 'label2'
        }
        label3 {
            text: 'label3'
        }
    }

    mouse_area {
        onClicked: {
            if (root.show_menu == false) {
                slider.state = "Visible"
                root.show_menu = true
            } else {
                slider.state = "Invisible"
                root.show_menu = false
            }
        }
    }
}