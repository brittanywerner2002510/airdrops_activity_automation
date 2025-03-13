import QtQuick 2.0
import QtQuick.Controls 6.3

TabButton {
    property color frame_color: "#2e2f30"
    property color hovered_color: "#6d6d6e"
    property string tab_title
    property bool is_selected: false
    property int iconWidth: 20
    property int iconHeight: 20
    property string project_name

    property var icon_mapper: {
        "Aptos": "../../img/projects_logo/aptos.svg",
        "Layer Zero": "../../img/projects_logo/Layerzero.png",
        "Merkly": "../../img/projects_logo/merkly.png"
    }

    id: tab_button
    contentItem: Rectangle {
        id: tabRectangle
        color: tab_button.hovered ? hovered_color : frame_color
        anchors.fill: parent
        implicitWidth: Math.max(tab_text.width + 30, 80)
        implicitHeight: Math.max(tab_text.height + 10, 20)

        Rectangle {
            id: separator
            height: tab_button.height
            width: 3
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 0
            anchors.bottomMargin: 0
            anchors.topMargin: 0
            color: "#55aaff"
        }

        Rectangle {
            id: is_selected_highlight
            height: 3
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.bottomMargin: 0
            color: "#55aaff"
            visible: is_selected

        }

        Image {
            id: btn_icon
            source: icon_mapper[project_name]
            anchors.leftMargin: 5
            layer.enabled: false
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: separator.left
            sourceSize.height: iconHeight
            sourceSize.width: iconWidth
            height: iconHeight
            width: iconWidth
            fillMode: Image.PreserveAspectFit
            antialiasing: true
        }

        Text {
            id: tab_text
            anchors.left: btn_icon.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.leftMargin: 10
            text: tab_button.tab_title
            elide: Text.ElideRight
            color: "#c3cbdd"
            width: parent.width - close_tab_btn.background.width
        }

        TopBarBtn {
            id: close_tab_btn
            btn_icon_source: "../../img/icons/close_icon_white.svg"
            btn_color_clicked: "#cc0000"
            btn_color_hover: "#cc0000"
            btn_color_default: frame_color
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.rightMargin: 4
            height: tab_button.height - 8
            width: tab_button.height - 8
            onClicked: tabBar.close_tab(tab_button.tab_title, tab_button.project_name);
        }
    }

    onFocusChanged: {
        if (activeFocus === true) {
            is_selected = true
        } else {
            is_selected = false
        }
    }
}
