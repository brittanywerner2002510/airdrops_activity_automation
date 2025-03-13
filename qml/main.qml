import QtQuick
import QtQuick.Window
import QtQuick.Controls 6.3
import QtQuick.Layouts 6.3
import QtQuick.Dialogs
import QtCore
import "controls"
import "projects"


Window {
    id: main_window
    width: 1366
    height: 768
    visible: true
    color: "#00000000"
    title: qsTr("AirDrop Activities Automation")

    flags: Qt.Window | Qt.FramelessWindowHint

    property bool is_window_max: false
    property bool file_dialog_open: false
    property int window_margin: 10
    property bool is_select_all: true
    property bool is_left_bar_full: false
    property bool is_accounts_list_hide: false

    MessageBox {
        id: message_box
        x: main_window.x + main_window.width / 2 - 150
        y: main_window.y + main_window.height / 2 - 75
        visible: false

        onAccepted: {
            message_box.close()
            backend.stop_tab(message_box.tab_name)
        }
    }

    LoadConfigDialog {
        id: load_config_dialog
        visible: false

        onAccepted: {
            load_config_dialog.close()
            backend.add_project_on_tab_bar(load_config_dialog.project_name, load_config_dialog.settings_name)
        }
    }

    Settings {
        property alias x: main_window.x
        property alias y: main_window.y
        property alias width: main_window.width
        property alias height: main_window.height
    }

    Connections {
        target: backend

        function onSetDatetime(current_datetime) {
            current_datetime_lbl.text = current_datetime
        }

        function onUpdateGas(gas_update) {
            current_gas_lbl.text = `ETH ${gas_update}`

            if (Number(gas_update) >= 20) {
                current_gas_lbl.color = "#ff0000"
            } else if (Number(gas_update) >= 15) {
                current_gas_lbl.color = "#ffd700"
            } else {
                current_gas_lbl.color = "#c3cbdd"
            }
        }

        function onAddTab(tab_name, project_name, config_name) {
          let new_view = tabBar.createTab(tab_name, project_name, config_name)
            backend.save_tab(new_view)
        }

        function onTabClose(tab_name, project_name) {
            tabBar.remove_view(tab_name, project_name)
        }

        function onShowMessageBox(tab_title, project_name) {
            message_box.tab_name = tab_title
            message_box.project_name = project_name
            message_box.visible = true
        }

        function onLoadConfigs(project_name, configs) {
            if (configs.length === 0) {
                backend.add_project_on_tab_bar(project_name, "default")
            } else {
                load_config_dialog.configs = configs
                load_config_dialog.project_name = project_name
                load_config_dialog.visible = true
            }
        }
    }

    QtObject {
        id: internal

        function maximizeRestore() {
            if(is_window_max == false) {
                window_margin = 0
                main_window.showMaximized()
                is_window_max = true
                maximize_btn.btn_icon_source = "../../img/icons/maximize_restore_icon_white.svg"
                resize_left.visible = false
                resize_right.visible = false
                resize_bottom.visible = false
                resize_top.visible = false
                resize_left_bottom.visible = false
                resize_right_bottom.visible = false
                resize_let_top.visible = false
                resize_right_top.visible = false
            }
            else {
                window_margin = 10
                main_window.showNormal()
                is_window_max = false
                maximize_btn.btn_icon_source = "../../img/icons/maximize_icon_white.svg"
                visible_resize_cursors()
            }
        }

        function if_maximized_window_restored() {
            if (is_window_max == true) {
                main_window.showNormal()
                restore_margin()
                visible_resize_cursors()
            }
        }

        function restore_margin() {
            is_window_max = false
            window_margin = 10
            maximize_btn.btn_icon_source = "../../img/icons/maximize_icon_white.svg"
        }

        function visible_resize_cursors() {
            resize_left.visible = true
            resize_right.visible = true
            resize_bottom.visible = true
            resize_top.visible = true
            resize_left_bottom.visible = true
            resize_right_bottom.visible = true
            resize_let_top.visible = true
            resize_right_top.visible = true
        }

        function get_accounts_switch_status() {
            var name;
            var element;
            var active_packs = []
            for (let i = 0; i < pack_list.count; i++) {
                element = pack_list.itemAtIndex(i)
                if(element.checked === true) {
                    name = element.objectName
                    active_packs.push(name)
                }
            }
            backend.get_active_accounts(active_packs)
        }

        function change_packs_switch_status() {
            var element;
            var i;
            if (is_select_all === true) {
                for (let i = 0; i < pack_list.count; i++) {
                    element = pack_list.itemAtIndex(i)
                    element.checked = false
                }
                is_select_all = false
            } else {
                for (let i = 0; i < pack_list.count; i++) {
                    element = pack_list.itemAtIndex(i)
                    element.checked = true
                }
                is_select_all = true
            }
        }

        function clear_list_view() {
            list_model.clear()
            select_all.visible = false
        }

        function show_hide_packs_list_handler() {
            var element;
            accounts_list_animation.running = true
            for (let i = 0; i < pack_list.count; i++) {
                element = pack_list.itemAtIndex(i)
                if (element.visible === true) {
                    element.visible = false
                    select_all.visible = false
                } else {
                    element.visible = true
                    select_all.visible = true
                }
            }
        }
    }

    MouseArea {
        id: resize_left
        width: 10
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        cursorShape: Qt.SizeHorCursor

        DragHandler {
            target: null
            onActiveChanged: if (active) {
                                 main_window.startSystemResize(Qt.LeftEdge)
                             }
        }
    }

    MouseArea {
        id: resize_right
        width: 10
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        cursorShape: Qt.SizeHorCursor

        DragHandler {
            target: null
            onActiveChanged: if (active) {
                                 main_window.startSystemResize(Qt.RightEdge)
                             }
        }
    }

    MouseArea {
        id: resize_top
        height: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.topMargin: 0
        cursorShape: Qt.SizeVerCursor

        DragHandler {
            target: null
            onActiveChanged: if (active) {
                                 main_window.startSystemResize(Qt.TopEdge)
                             }
        }
    }

    MouseArea {
        id: resize_bottom
        width: 10
        height: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: 10
        anchors.bottomMargin: 0
        anchors.rightMargin: 10
        cursorShape: Qt.SizeVerCursor

        DragHandler {
            target: null
            onActiveChanged: if (active) {
                                 main_window.startSystemResize(Qt.BottomEdge)
                             }
        }
    }

    MouseArea {
        id: resize_right_bottom
        width: 25
        height: 25
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        cursorShape: Qt.SizeFDiagCursor

        DragHandler {
            target: null
            onActiveChanged: if (active) {
                                 main_window.startSystemResize(Qt.RightEdge | Qt.BottomEdge)
                             }
        }
    }

    MouseArea {
        id: resize_right_top
        width: 25
        height: 25
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 0
        anchors.topMargin: 0
        cursorShape: Qt.SizeBDiagCursor

        DragHandler {
            target: null
            onActiveChanged: if (active) {
                                 main_window.startSystemResize(Qt.RightEdge | Qt.TopEdge)
                             }
        }
    }

    MouseArea {
        id: resize_let_top
        width: 25
        height: 25
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 0
        anchors.topMargin: 0
        cursorShape: Qt.SizeFDiagCursor

        DragHandler {
            target: null
            onActiveChanged: if (active) {
                                 main_window.startSystemResize(Qt.LeftEdge | Qt.TopEdge)
                             }
        }
    }

    MouseArea {
        id: resize_left_bottom
        width: 25
        height: 25
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        cursorShape: Qt.SizeBDiagCursor

        DragHandler {
            target: null
            onActiveChanged: if (active) {
                                 main_window.startSystemResize(Qt.LeftEdge | Qt.BottomEdge)
                             }
        }
    }

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

        Rectangle {
            id: app_container
            color: "#00000000"
            anchors.fill: parent
            anchors.rightMargin: 1
            anchors.leftMargin: 1
            anchors.bottomMargin: 1
            anchors.topMargin: 1

            Rectangle {
                id: top_bar
                height: 60
                color: "#1f1f1f"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.topMargin: 0

                ToggleBtn {
                    id: toggle_btn
                    onClicked: {
                        left_bar_animation.running = true
                        if(is_left_bar_full == false) {
                            is_left_bar_full = true
                            btn_icon_source = "../../img/icons/close_icon_white.svg"
                        } else {
                            is_left_bar_full = false
                            btn_icon_source = "../../img/icons/menu_icon_white.svg"
                        }
                    }
                }

                Rectangle {
                    id: top_bar_description
                    y: 35
                    height: 25
                    color: "#2e2f30"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 70
                    anchors.bottomMargin: 0

                    Label {
                        id: description_lbl
                        color: "#5f6a82"
                        text: qsTr("App to perform activities to get AirDrop")
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 10
                        anchors.bottomMargin: 0
                        anchors.rightMargin: 300
                        anchors.leftMargin: 10
                        anchors.topMargin: 0
                    }

                    Rectangle {
                        id: rectangle
                        color: "#2e2f30"
                        anchors.left: description_lbl.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0

                        Label {
                            id: label
                            x: 0
                            width: 91
                            height: 16
                            color: "#c3cbdd"
                            text: qsTr("Current GAS:")
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: current_gas_lbl.left
                            anchors.rightMargin: 15
                            font.pointSize: 10
                            font.family: "Verdana"
                        }

                        Label {
                            id: current_gas_lbl
                            width: 58
                            height: 16
                            text: qsTr("0")
                            color: "#c3cbdd"
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            anchors.rightMargin: 20
                            anchors.verticalCenterOffset: 0
                            font.pointSize: 10
                            font.family: "Verdana"
                        }
                    }
                }

                Rectangle {
                    id: title_bar
                    height: 35
                    color: "#00000000"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: 105
                    anchors.leftMargin: 70
                    anchors.topMargin: 0

                    DragHandler {
                        onActiveChanged: if(active){
                                             main_window.startSystemMove()
                                             internal.if_maximized_window_restored()
                                         }
                    }

                    Image {
                        id: app_icon
                        width: 28
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        source: "../img/icons/payments_icon.svg"
                        anchors.leftMargin: 5
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        fillMode: Image.PreserveAspectFit
                    }

                    Label {
                        id: title_lbl
                        color: "#c3cbdd"
                        text: qsTr("AirDrop Activities Automation")
                        anchors.left: app_icon.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 10
                        anchors.leftMargin: 10
                    }
                }

                Row {
                    id: managing_btns_row
                    x: 1153
                    width: 105
                    height: 35
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: 0
                    anchors.topMargin: 0

                    TopBarBtn {
                        id: minimize_btn
                        scale: 1
                        btn_icon_source: "../../img/icons/minimize_icon_white.svg"
                        onClicked: {
                            main_window.showMinimized()
                            internal.restore_margin()
                        }
                    }

                    TopBarBtn {
                        id: maximize_btn
                        width: 35
                        height: 35
                        scale: 1
                        btn_icon_source: "../../img/icons/maximize_icon_white.svg"
                        onClicked: internal.maximizeRestore()
                    }

                    TopBarBtn {
                        id: close_btn
                        btn_icon_source: "../../img/icons/close_icon_white.svg"
                        btn_color_clicked: "#D85A5A"
                        btn_color_hover: "#ff0000"
                        onClicked: main_window.close()
                    }
                }
            }

            Rectangle {
                id: content
                color: "#00000000"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: top_bar.bottom
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.topMargin: 0

                Rectangle {
                    id: left_bar
                    width: 70
                    visible: true
                    color: "#1f1f1f"
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    clip: true
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0

                    PropertyAnimation {
                        id: left_bar_animation
                        target: left_bar
                        property: "width"
                        to: left_bar.width == 250 ? 70 : 250
                        duration: 1000
                        easing.type: Easing.InOutQuint
                    }

                    Column {
                        id: project_btns_column
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 0
                        anchors.leftMargin: 0
                        anchors.bottomMargin: 166
                        anchors.topMargin: 0

                        ProjectsBtn {
                            id: layer_zero_btn
                            btn_icon_source: "../../img/projects_logo/Layerzero.png"
                            width: left_bar.width
                            text: qsTr("Layer Zero")
                            font.pointSize: 13
                            font.family: "Verdana"

                            onClicked: {
                                backend.load_configs("Layer Zero")
                            }
                        }

                        ProjectsBtn {
                            id: aptos_btn
                            btn_icon_source: "../../img/projects_logo/aptos.svg"
                            width: left_bar.width
                            text: qsTr("Aptos")
                            font.family: "Verdana"
                            font.pointSize: 13

                            onClicked: {
                                backend.load_configs("Aptos")
                            }
                        }

                        ProjectsBtn {
                            id: merkly_btn
                            btn_icon_source: "../../img/projects_logo/merkly.png"
                            width: left_bar.width
                            text: qsTr("Merkly")
                            font.family: "Verdana"
                            font.pointSize: 13

                            onClicked: {
                                backend.load_configs("Merkly")
                            }
                        }
                    }
                }

                Rectangle {
                    id: content_pages
                    color: "#00000000"
                    anchors.left: left_bar.right
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 6
                    anchors.bottomMargin: 25
                    anchors.topMargin: 0

                    Rectangle {
                        id: tab_content
                        color: "#2e2f30"
                        anchors.fill: parent
                        anchors.rightMargin: 10
                        anchors.leftMargin: 10
                        anchors.bottomMargin: 10
                        anchors.topMargin: 10
                        clip: true

                        StackLayout {
                            id: tabLayout
                            currentIndex: tabBar.currentIndex
                            anchors.top: tabBar.bottom
                            anchors.bottom: parent.bottom
                            anchors.left: parent.left
                            anchors.right: parent.right
                        }

                        Component {
                            id: tabButtonComponent

                            ProjectTabButton {
                                id: project_tab_btn
                                width: Math.max(100, tabBar.width / 9)
                            }
                        }

                        TabBar {
                            id: tabBar
                            anchors.top: parent.top
                            anchors.left: parent.left
                            anchors.right: parent.right

                            function createTab(tab_name, project_name, config_name, focusOnNewTab = true) {
                                const projects_map = {
                                    "Layer Zero": layerzero_component,
                                    "Aptos": aptos_component,
                                    "Merkly": merkly_component
                                }

                                var webview = projects_map[project_name].createObject(tabLayout);
                                webview.tab_name = tab_name
                                webview.settings_name = config_name
                                var newTabButton = tabButtonComponent.createObject(tabBar, {tab_title: tab_name, project_name: project_name});
                                tabBar.addItem(newTabButton);
                                if (focusOnNewTab) {
                                    tabBar.setCurrentIndex(tabBar.count - 1);
                                }
                                return webview;
                            }

                            function remove_view(tab_title, project_name) {
                                var _contentData = tabBar.contentChildren
                                for (var i = 0; i < _contentData.length; i++) {
                                    if ( _contentData[i]['tab_title'] === tab_title) {
                                        var _removeItem = tabBar.itemAt(i)
                                        tabBar.removeItem(_removeItem)
                                        tabLayout.children[i].destroy()
                                    }
                                }
                                tabBar.setCurrentIndex(0)
                                backend.remove_tab(project_name, tab_title)
                            }

                            function close_tab(tab_title, project_name) {
                                backend.close_tab(tab_title, project_name)
                            }

                            Component {
                                id: layerzero_component

                                LayerZero {
                                    id: layerzero_tab
                                    flickable_height: main_window.height === Screen.desktopAvailableHeight ? default_settings_space_height * 1.2 : default_settings_space_height * 1.2
                                }
                            }

                            Component {
                                id: aptos_component

                                Aptos {
                                    id: aptos_tab
                                    flickable_height: main_window.height === Screen.desktopAvailableHeight ? default_settings_space_height * 1.15 : default_settings_space_height * 1.15
                                }
                            }

                            Component {
                                id: merkly_component

                                Merkly {
                                    id: merkly_tab
                                    flickable_height: main_window.height === Screen.desktopAvailableHeight ? default_settings_space_height * 1.15 : default_settings_space_height * 1.15
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    id: footer
                    color: "#262728"
                    anchors.left: left_bar.right
                    anchors.right: parent.right
                    anchors.top: content_pages.bottom
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 0
                    anchors.topMargin: 0

                    Label {
                        id: current_datetime_lbl
                        x: 42
                        color: "#5f6a82"
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        verticalAlignment: Text.AlignVCenter
                        font.family: "Verdana"
                        anchors.rightMargin: 10
                        anchors.topMargin: 0
                        font.pointSize: 10
                        anchors.leftMargin: 10
                        anchors.bottomMargin: 0
                    }
                }
            }
        }
    }
}
