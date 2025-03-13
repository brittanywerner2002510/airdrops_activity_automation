import QtQuick 2.15
import QtQuick.Controls 2.15

Window {
    property string tab_name
    property string project_name

    signal accepted

    id: message_box
    width: 300
    height: 150
    color: "#00000000"
    modality: Qt.ApplicationModal
    flags: Qt.Dialog
    maximumHeight: 150
    maximumWidth: 300
    minimumHeight: 150
    minimumWidth: 300
    title: "Close tab"

    Rectangle {
        id: background
        color: "#2e2f30"
        radius: 0
        border.color: "#383e4c"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0

        TextArea {
            id: text_area
            color: "#81848c"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            text: `Are you sure you want to close the tab ${tab_name}?`
            font.pixelSize: 16
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.family: "Verdana"
            readOnly: true
            wrapMode: Text.WordWrap
            anchors.rightMargin: 10
            anchors.leftMargin: 10
            anchors.bottomMargin: 50
            anchors.topMargin: 10
            background: Rectangle {
                id: output_background
                color: "#2e2f30"
            }
        }

        RunBtn {
            id: yes_btn
            width: 70
            height: 30
            text: "Yes"
            anchors.bottom: parent.bottom
            anchors.horizontalCenterOffset: -45
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: 10

            onClicked: {
                accepted()
            }
        }

        RunBtn {
            id: no_btn
            width: 70
            height: 30
            text: "No"
            anchors.bottom: parent.bottom
            anchors.horizontalCenterOffset: 45
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: 10

            onClicked: message_box.close()
        }
    }
}
