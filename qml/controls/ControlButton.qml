import QtQuick 2.15
import QtQuick.Controls 6.3


Button {
    id: settings_button
    text: qsTr("Settings")
    property url btn_icon_source

    property color btn_color_default: "#1f1f1f"
    property color btn_color_hover: "#55aaff"
    property color btn_color_clicked: "#00a1f1"
    property color active_menu_color: "#55aaff"
    property int iconWidth: 35
    property int iconHeight: 35
    property bool is_active: true

    width: 250
    height: 60
    flat: true

    background: Rectangle {
        id: btn_background
        color: settings_button.down ? btn_color_clicked : settings_button.hovered ? btn_color_hover : btn_color_default

        Rectangle {
            anchors {
                top: parent.top
                left: parent.left
                bottom: parent.bottom
            }
            color: active_menu_color
            width: 3
            visible: is_active
        }
    }

    contentItem: Item {
        anchors.fill: parent
        id: content

        Image {
            id: btn_icon
            source: btn_icon_source
            anchors.leftMargin: 20
            layer.enabled: false
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            sourceSize.height: iconHeight
            sourceSize.width: iconWidth
            height: iconHeight
            width: iconWidth
            fillMode: Image.PreserveAspectFit
            antialiasing: true
        }

        Text {
            color: "#ffffff"
            text: settings_button.text
            font: settings_button.font
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 75
        }
    }
}
