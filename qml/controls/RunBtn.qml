import QtQuick 2.15
import QtQuick.Controls 6.3


Button {
    id: run_btn
    text: qsTr("Run")

    property color btn_color_default: "#2e2f30"
    property color btn_color_hover: "#55aaff"
    property color btn_color_clicked: "#00a1f1"

    width: 200
    height: 60
    flat: true

    background: Rectangle {
        id: btn_background
        radius: 12
        border.width: 2
        border.color: "#55aaff"
        color: run_btn.down ? btn_color_clicked : run_btn.hovered ? btn_color_hover : btn_color_default
    }

    contentItem: Item {
        anchors.fill: parent
        id: content

        Text {
            color: "#ffffff"
            text: run_btn.text
            font: run_btn.font
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
