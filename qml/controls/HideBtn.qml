import QtQuick 2.15
import QtQuick.Controls 6.3


Button {
    id: show_hide_btn

    property url btn_icon_source: "../../img/icons/hide_icon.svg"

    width: 25
    height: 25
    flat: true

    background: Rectangle {
        id: btn_background
        color: "#2e2f30"

        Image {
            id: btn_icon
            source: btn_icon_source
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 18
            width: 18
            fillMode: Image.PreserveAspectFit
            antialiasing: false
        }
    }
}
