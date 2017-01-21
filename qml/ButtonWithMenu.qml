import QtQuick 2.0

MyButton {
    id: root
    property bool show_menu: false

    state: "Invisible"
    text: 'Button'

    property alias slider: slider

    Slider3D {
        id: slider
        state: "Invisible"
        anchors.top: parent.top
        anchors.left: parent.right

        text1: 'label1'
        text2: 'label2'
        text3: 'label3'
        value1: 0.0
        value2: 0.0
        value3: 0.0

    }

    function onValueChanged(val1, val2, val3) {
        if (val1 != slider.value1)
            slider.value1 = val1
        if (val2 != slider.value2)
            slider.value2 = val2
        if (val3 != slider.value3)
            slider.value3 = val3
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