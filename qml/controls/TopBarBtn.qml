import QtQuick 2.15
import QtQuick.Controls 6.3


Button {
    id: minimize_btn
    property url btn_icon_source: "../../img/icons/minimize_icon_white.svg"
    property color btn_color_default: "#1f1f1f"
    property color btn_color_hover: "#08091a"
    property color btn_color_clicked: "#00a1f1"
    property int icon_width: 16
    property int icon_height: 16

    width: 35
    height: 35
    flat: true

    background: Rectangle {
        id: btn_background
        color: minimize_btn.down ? btn_color_clicked : minimize_btn.hovered ? btn_color_hover : btn_color_default
        border.color: minimize_btn.down ? btn_color_clicked : minimize_btn.hovered ? btn_color_hover : btn_color_default
        height: parent.height
        width: parent.width

        Image {
            id: btn_icon
            source: btn_icon_source
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 16
            width: 16
            fillMode: Image.PreserveAspectFit
            antialiasing: false
        }
    }
}
