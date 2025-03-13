import QtQuick 2.15
import QtQuick.Controls 6.3


Button {
    id: select_file_btn
    property url btn_icon_source: "../../img/icons/folder_icon.svg"
    property bool is_valid: true

    property color btn_color_default: "#2e2f30"
    property color btn_color_hover: "#2B2F38"
    property color btn_color_clicked: "#242831"
    property color btn_color_error: "#ff0000"

    width: 50
    height: 40
    flat: true

    background: Rectangle {
        id: btn_background
        color: select_file_btn.down ? btn_color_clicked : select_file_btn.hovered ? btn_color_hover : btn_color_default
        border.color: is_valid ? btn_background.color : btn_color_error
        border.width: 2
        radius: 6

        Image {
            id: btn_icon
            source: btn_icon_source
            layer.enabled: false
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 40
            width: 50
            fillMode: Image.PreserveAspectFit
        }
    }
}
