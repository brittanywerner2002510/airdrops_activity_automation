import QtQuick 2.15
import QtQuick.Controls 2.15

Window {
    property string project_name
    property string settings_name
    property var configs: []

    signal accepted

    id: save_config_dialog
    width: 350
    height: 160
    color: "#00000000"
    modality: Qt.ApplicationModal
    flags: Qt.Dialog
    maximumHeight: 150
    maximumWidth: 300
    minimumHeight: 150
    minimumWidth: 300
    title: `Select config for ${project_name}`

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

        ChainSelector {
            id: configs_cb
            width: 200
            height: 28
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            model: configs
        }

        RunBtn {
            id: ok_btn
            width: 70
            height: 30
            text: "OK"
            anchors.bottom: parent.bottom
            anchors.horizontalCenterOffset: 0
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: 10

            onClicked: {
                save_config_dialog.settings_name = configs_cb.currentText
                accepted()
            }
        }
    }
}
