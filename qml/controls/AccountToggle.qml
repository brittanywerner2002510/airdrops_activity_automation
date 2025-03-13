import QtQuick 2.15
import QtQuick.Controls 6.3

Switch {
    id: account_switch

    property color checked_color: "#55aaff"
    property var switch_text_field: ""
    property int switch_height: 20
    property int switch_width: 40
    property bool switch_visible: true
    checked: true

    contentItem: Text {
        id: switch_text
        text: switch_text_field
        anchors.verticalCenter: indicator.verticalCenter
        anchors.left: indicator.right
        anchors.leftMargin: 5
        font.pointSize: 10
        font.family: "Verdana"
        color: account_switch.checked ? checked_color : "#ffffff"
    }

    indicator: Rectangle {
        id: indicator
        width: switch_width
        height: switch_height
        radius: height / 2
        color: account_switch.checked ? checked_color : "#ffffff"
        border.width: 2
        anchors.verticalCenter: parent.verticalCenter
        border.color: account_switch.checked ? checked_color : "#ffffff"
        visible: switch_visible

        Rectangle {
            x: account_switch.checked ? parent.width - width - 2 : 1
            width: account_switch.checked ? parent.height - 4 : parent.height - 2
            height: width
            radius: width / 2
            color: "#ffffff"
            border.color: "#D5D5D5"
            anchors.verticalCenter: parent.verticalCenter

            Behavior on x {
                NumberAnimation {
                    duration: 200
                }
            }
        }
    }
}
