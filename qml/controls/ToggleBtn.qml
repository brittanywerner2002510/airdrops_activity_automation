import QtQuick 2.15
import QtQuick.Controls 6.3


Button {
    id: toggle_btn
    property url btn_icon_source: "../../img/icons/menu_icon_white.svg"
    property color btn_color_default: "#1f1f1f"
    property color btn_color_hover: "#55aaff"
    property color btn_color_clicked: "#00a1f1"

    width: 70
    height: 60
    flat: true

    background: Rectangle {
        id: btn_background
        color: toggle_btn.down ? btn_color_clicked : toggle_btn.hovered ? btn_color_hover : btn_color_default

        Image {
            id: btn_icon
            source: btn_icon_source
            layer.enabled: false
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 25
            width: 25
            fillMode: Image.PreserveAspectFit
        }
    }
}
