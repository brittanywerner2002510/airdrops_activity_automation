import QtQuick
import QtCore
import QtQuick.Window
import QtQuick.Controls 6.3
import QtQuick.Layouts 6.3
import QtQuick.Dialogs
import Qt.labs.settings 1.1
import "../controls"


Rectangle {
    id: merkly_window
    width: 1920
    height: 1080
    visible: true
    color: "#00000000"

    property bool is_window_max: false
    property bool file_dialog_open: false
    property int window_margin: 10
    property bool is_select_all: false
    property bool is_left_bar_full: false
    property bool is_accounts_list_hide: false
    property int flickable_height: 566
    property string tab_name
    property string settings_name
    property int default_settings_space_height: general_settings_space.height + input_space.height +
                                                run_btn.height + time_setter_space.height
    property var source_networks: [
        "Arbitrum",
        "Arbitrum Nova",
        "Avalanche",
        "Base",
        "BSC",
        "Canto",
        "Celo",
        "Coredao",
        "DFK",
        "Fantom",
        "Fuse",
        "Gnosis",
        "Harmony One",
        "Kava",
        "Klaytn",
        "Linea",
        "Mantle",
        "Meter",
        "Metis",
        "Moonbeam",
        "Moonriver",
        "OKEX Chain",
        "Optimism",
        "Polygon",
        "Polygon zkEVM",
        "Sepolia",
        "Tenet",
        "zkSync Era",
        "Zora"
    ]

    PropertyAnimation {
        id: accounts_list_animation
        target: pack_list
        property: "width"
        to: pack_list.width === 220 ? 0 : 220
        duration: 500
        easing.type: Easing.InOutQuint
    }

    SaveConfigDialog {
        id: save_config_dialog
        visible: false

        onAccepted: {
            close()
            backend.save_config(save_config_dialog.project_name, merkly_window.settings_name, save_config_dialog.settings_name)
        }
    }

    Settings {
        id: merkly_settings
        fileName: `settings/Merkly/${settings_name}`

        property alias max_gas_fee_field: max_gas_fee_field.text

        property alias input_min_field: input_min_field.text
        property alias input_max_field: input_max_field.text
        property alias source_network_cb: source_network_cb.currentIndex
        property alias destination_network_cb_model: destination_network_cb.model
        property alias destination_network_cb_current_index: destination_network_cb.currentIndex

        property alias time_from_field: time_from_field.text
        property alias time_to_field: time_to_field.text
        property alias time_from_field_enabled: time_from_field.enabled
        property alias time_to_field_enabled: time_to_field.enabled
        property alias time_from_field_opacity: time_from_field.opacity
        property alias time_to_field_opacity: time_to_field.opacity
        property alias asap_toggle: asap_toggle.checked
    }

    Connections {
        target: backend

        function onAddAccount(pack, model_object, required_tab) {
            let content_child = content_pages.children
            for (var i = 0; i < content_child.length; i++) {
                if ( content_child[i].objectName === `select_all_${required_tab}` || content_child[i].objectName === `shuffle_wallets_${required_tab}`) {
                    content_child[i].visible = true
                }
            }
            model_object.model = pack
        }

        function onTimeValidator(is_time_valid) {

            time_from_field.is_valid = is_time_valid
            time_to_field.is_valid = is_time_valid

            if (is_time_valid === false) {
                run_btn.enabled = false
                run_btn.opacity = 0.5
            } else {
                run_btn.enabled = true
                run_btn.opacity = 1
            }
        }

        function onTabFinish(tab_title) {
            if (tab_title === tab_name) {
                run_btn.enabled = true
                run_btn.opacity = 1
            }
        }
    }

    DoubleValidator {
        id: percent_validator
        bottom: 0.0
        top: 100.0
        locale: "en_EN"
    }

    QtObject {
        id: internal

        property var networks_match: {
            "Arbitrum": [
                    "Arbitrum Nova",
                    "Avalanche",
                    "Base",
                    "BSC",
                    "Canto",
                    "Celo",
                    "DFK",
                    "Gnosis",
                    "Harmony One",
                    "Kava",
                    "Linea",
                    "Mantle",
                    "Meter",
                    "Moonbeam",
                    "Moonriver",
                    "OKEX Chain",
                    "Optimism",
                    "Polygon",
                    "Polygon zkEVM",
                    "Sepolia",
                    "Tenet",
                    "zkSync Era",
                    "Zora"
                ],
            "Arbitrum Nova": [
                    "Arbitrum",
                    "Avalanche",
                    "BSC",
                    "Canto",
                    "Celo",
                    "Coredao",
                    "Fantom",
                    "Fuse",
                    "Meter",
                    "Metis",
                    "Moonbeam",
                    "Moonriver",
                    "OKEX Chain",
                    "Optimism",
                    "Polygon",
                    "Tenet",
                    "zkSync Era"
                ],
            "Avalanche": [
                    "Arbitrum",
                    "Arbitrum Nova",
                    "Base",
                    "BSC",
                    "Canto",
                    "Celo",
                    "DFK",
                    "Fantom",
                    "Fuse",
                    "Gnosis",
                    "Harmony One",
                    "Kava",
                    "Klaytn",
                    "Linea",
                    "Mantle",
                    "Meter",
                    "Metis",
                    "Moonbeam",
                    "Moonriver",
                    "OKEX Chain",
                    "Optimism",
                    "Polygon",
                    "Polygon zkEVM",
                    "Tenet",
                    "zkSync Era"
                ],
            "Base": [
                    "Arbitrum",
                    "Avalanche",
                    "BSC",
                    "Fantom",
                    "Kava",
                    "Linea",
                    "Mantle",
                    "Metis",
                    "Optimism",
                    "Polygon",
                    "Polygon zkEVM",
                ],
            "BSC": [
                    "Arbitrum",
                    "Arbitrum Nova",
                    "Avalanche",
                    "Base",
                    "Canto",
                    "Celo",
                    "Coredao",
                    "DFK",
                    "Fantom",
                    "Gnosis",
                    "Harmony One",
                    "Kava",
                    "Linea",
                    "Mantle",
                    "Meter",
                    "Metis",
                    "Moonbeam",
                    "Moonriver",
                    "OKEX Chain",
                    "Optimism",
                    "Polygon",
                    "Polygon zkEVM",
                    "Tenet",
                    "zkSync Era",
                ],
            "Canto": [
                    "Arbitrum",
                    "Arbitrum Nova",
                    "Avalanche",
                    "BSC",
                    "Fantom",
                    "Meter",
                    "Metis",
                    "Optimism",
                    "Polygon",
                    "Tenet",
                    "zkSync Era",
                ],
            "Celo": [
                    "Arbitrum",
                    "Avalanche",
                    "BSC",
                    "Fantom",
                    "Gnosis",
                    "Optimism",
                    "Polygon"
                ],
            "Coredao": [
                    "BSC",
                    "Polygon"
                ],
            "DFK": [
                    "Arbitrum",
                    "Avalanche",
                    "BSC",
                    "Fantom",
                    "Harmony One",
                    "Klaytn",
                    "Moonbeam",
                    "Polygon"
                ],
            "Fantom": [
                    "Arbitrum",
                    "Arbitrum Nova",
                    "Avalanche",
                    "Base",
                    "BSC",
                    "Canto",
                    "Celo",
                    "DFK",
                    "Gnosis",
                    "Harmony One",
                    "Kava",
                    "Linea",
                    "Mantle",
                    "Meter",
                    "Metis",
                    "Moonbeam",
                    "Moonriver",
                    "Optimism",
                    "Polygon",
                    "Tenet",
                    "zkSync Era"
                ],
            "Fuse": [
                    "Avalanche",
                    "Gnosis",
                    "Klaytn",
                    "Metis"
                ],
            "Gnosis": [
                    "Arbitrum",
                    "Avalanche",
                    "BSC",
                    "Celo",
                    "Fantom",
                    "Fuse",
                    "Klaytn",
                    "Metis",
                    "Optimism",
                    "Polygon"
                ],
            "Harmony One": [
                    "Arbitrum",
                    "Avalanche",
                    "BSC",
                    "Fantom",
                    "Moonbeam",
                    "Optimism",
                    "Polygon"
                ],
            "Kava": [
                    "Arbitrum",
                    "Avalanche",
                    "Base",
                    "BSC",
                    "Fantom",
                    "Linea",
                    "Metis",
                    "Optimism",
                    "Polygon"
                ],
            "Linea": [
                    "Arbitrum",
                    "Avalanche",
                    "Base",
                    "BSC",
                    "Fantom",
                    "Kava",
                    "Mantle",
                    "Metis",
                    "Polygon",
                    "Polygon zkEVM"
                ],
            "Mantle": [
                    "Arbitrum",
                    "Avalanche",
                    "Base",
                    "BSC",
                    "Fantom",
                    "Linea",
                    "Metis",
                    "Optimism",
                    "Polygon",
                    "Polygon zkEVM"
                ],
            "Meter": [
                    "Arbitrum",
                    "Arbitrum Nova",
                    "Avalanche",
                    "BSC",
                    "Canto",
                    "Fantom",
                    "Metis",
                    "Optimism",
                    "Polygon",
                    "Tenet",
                    "zkSync Era"
                ],
            "Metis": [
                    "Arbitrum Nova",
                    "Avalanche",
                    "Base",
                    "BSC",
                    "Canto",
                    "Fantom",
                    "Fuse",
                    "Gnosis",
                    "Kava",
                    "Klaytn",
                    "Linea",
                    "Mantle",
                    "Meter",
                    "Moonriver",
                    "Tenet"
                ],
            "Moonbeam": [
                    "Arbitrum",
                    "Avalanche",
                    "BSC",
                    "DFK",
                    "Fantom",
                    "Harmony One",
                    "Optimism",
                    "Polygon"
                ],
            "Moonriver": [
                    "Arbitrum",
                    "Avalanche",
                    "BSC",
                    "Fantom",
                    "Metis",
                    "Optimism",
                    "Polygon"
                ],
            "OKEX Chain": [
                    "Arbitrum",
                    "Avalanche",
                    "BSC",
                    "Polygon"
                ],
            "Optimism": [
                    "Arbitrum",
                    "Arbitrum Nova",
                    "Avalanche",
                    "Base",
                    "BSC",
                    "Canto",
                    "Celo",
                    "DFK",
                    "Fantom",
                    "Gnosis",
                    "Harmony One",
                    "Kava",
                    "Klaytn",
                    "Linea",
                    "Mantle",
                    "Meter",
                    "Moonbeam",
                    "Moonriver",
                    "Polygon",
                    "Polygon zkEVM",
                    "Sepolia",
                    "Tenet",
                    "zkSync Era"
                ],
            "Polygon": [
                    "Arbitrum",
                    "Arbitrum Nova",
                    "Avalanche",
                    "Base",
                    "BSC",
                    "Canto",
                    "Celo",
                    "Coredao",
                    "DFK",
                    "Fantom",
                    "Gnosis",
                    "Harmony One",
                    "Kava",
                    "Linea",
                    "Mantle",
                    "Meter",
                    "Moonbeam",
                    "Moonriver",
                    "OKEX Chain",
                    "Optimism",
                    "Polygon zkEVM",
                    "Tenet",
                    "zkSync Era"
                ],
            "Polygon zkEVM": [
                    "Arbitrum",
                    "Avalanche",
                    "Base",
                    "BSC",
                    "Linea",
                    "Mantle",
                    "Optimism",
                    "Polygon",
                    "zkSync Era"
                ],
            "Sepolia": [
                    "Arbitrum"
                ],
            "Tenet": [
                    "Arbitrum",
                    "Arbitrum Nova",
                    "Avalanche",
                    "BSC",
                    "Canto",
                    "Fantom",
                    "Meter",
                    "Metis",
                    "Optimism",
                    "Polygon",
                    "zkSync Era"
                ],
            "zkSync Era": [
                    "Arbitrum",
                    "Arbitrum Nova",
                    "Avalanche",
                    "BSC",
                    "Canto",
                    "Fantom",
                    "Meter",
                    "Optimism",
                    "Polygon",
                    "Polygon zkEVM",
                    "Tenet"
                ],
            "Zora": [
                    "Arbitrum",
                    "Base",
                    "Optimism",
                    "Polygon"
                ],
        }

        function get_accounts_switch_status() {
            var name;
            var element;
            var active_packs = []
            let packs_list = pack_list_flickable_zone.children
            for (let i = 0; i < packs_list.length; i++) {
                element = packs_list[i]
                if(element.checked === true) {
                    name = element.objectName
                    active_packs.push(name)
                }
            }
            backend.get_active_accounts(active_packs, shuffle_wallets.checked)
        }

        function change_packs_switch_status() {
            var element;
            var i
            let packs_list = pack_list_flickable_zone.children
            if (is_select_all === false) {
                for (i = 0; i < packs_list.length; i++) {
                    element = packs_list[i]
                    if (element.objectName !== `list_model_${tab_name}`) {
                        element.checked = true
                    }
                }
                is_select_all = true
            } else {
                for (i = 0; i < packs_list.length; i++) {
                    element = packs_list[i]
                    if (element.objectName !== `list_model_${tab_name}`) {
                        element.checked = false
                    }
                }
                is_select_all = false
            }
        }

        function clear_list_view() {
            list_model.model = []
            select_all.visible = false
            shuffle_wallets.visible = false
        }

        function show_hide_packs_list_handler() {
            var element;
            let accounts = pack_list_flickable_zone.children
            accounts_list_animation.running = true
            if (accounts.length > 2) {
                if (pack_list.visible === false) {
                    pack_list.visible = true
                    shuffle_wallets.visible = true
                    select_all.visible = true
                } else {
                    pack_list.visible = false
                    shuffle_wallets.visible = false
                    select_all.visible = false
                }
            }
        }

        function validation() {
            if (path_to_accounts_file.text === "") {
                path_to_accounts_file.is_valid = false
                run_btn.enabled = false
                run_btn.opacity = 0.5
                return false
            } else {
                path_to_accounts_file.is_valid = true
                run_btn.enabled = true
                run_btn.opacity = 1
            }

            if (max_gas_fee_field.text === "") {
                max_gas_fee_field.is_valid = false
                run_btn.enabled = false
                run_btn.opacity = 0.5
                return false
            } else {
                max_gas_fee_field.is_valid = true
                run_btn.enabled = true
                run_btn.opacity = 1
            }

            if (input_min_field.text === "") {
                input_min_field.is_valid = false
                run_btn.enabled = false
                run_btn.opacity = 0.5
                return false
            } else {
                input_min_field.is_valid = true
                run_btn.enabled = true
                run_btn.opacity = 1
            }

            if (input_max_field.text === "") {
                input_max_field.is_valid = false
                run_btn.enabled = false
                run_btn.opacity = 0.5
                return false
            } else {
                input_max_field.is_valid = true
                run_btn.enabled = true
                run_btn.opacity = 1
            }

            if (asap_toggle.checked === false) {
                if (time_from_field.text === ":" || time_to_field.text === ":") {
                    time_from_field.is_valid = false
                    time_to_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    time_from_field.is_valid = true
                    time_to_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }
            }

            return true
        }

        function lock_ui() {
            run_btn.enabled = false
            run_btn.opacity = 0.5
        }
    }

    FileDialog {
        id: file_dialog
        title: "Select file with accounts info"
        currentFolder: StandardPaths.standardLocations(StandardPaths.DocumentsLocation)[0]
        nameFilters: ["JSON Files (*.json)"]
        onAccepted: {
            path_to_accounts_file.text = selectedFile
            backend.file_handler(selectedFile, tab_name)
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

                Rectangle {
                    id: top_bar_description
                    y: 35
                    height: 25
                    color: "#2e2f30"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 0

                    Label {
                        id: description_lbl
                        color: "#5f6a82"
                        text: qsTr("AirDrop activities for Merkly")
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
                    anchors.leftMargin: 0
                    anchors.topMargin: 0

                    Image {
                        id: app_icon
                        width: 28
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        source: "../../img/projects_logo/merkly.png"
                        anchors.leftMargin: 5
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        fillMode: Image.PreserveAspectFit
                    }

                    Label {
                        id: title_lbl
                        color: "#c3cbdd"
                        text: qsTr("Merkly")
                        anchors.left: app_icon.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 10
                        anchors.leftMargin: 10
                    }

                    Label {
                        id: config_lbl
                        width: 150
                        color: "#c3cbdd"
                        text: settings_name
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        anchors.rightMargin: 10
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
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
                    id: content_pages
                    color: "#00000000"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 25
                    anchors.topMargin: 0

                    Rectangle {
                        id: file_content
                        height: 50
                        color: "#2e2f30"
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.rightMargin: 0
                        anchors.topMargin: 0
                        anchors.leftMargin: 30

                        CustomTextField {
                            id: path_to_accounts_file
                            width: 700
                            anchors.left: parent.left
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            font.pointSize: 10
                            anchors.leftMargin: 5
                            anchors.bottomMargin: 5
                            anchors.topMargin: 5

                            onTextChanged: {
                                if (text !== "") {
                                    is_valid = true
                                    run_btn.enabled = true
                                    run_btn.opacity = 1
                                }
                            }
                        }

                        SelectFileBtn {
                            id: select_file_btn
                            width: 50
                            anchors.left: path_to_accounts_file.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.leftMargin: 20
                            anchors.bottomMargin: 5
                            anchors.topMargin: 5

                            onClicked: {
                                if (is_accounts_list_hide == true) {
                                    internal.show_hide_packs_list_handler()
                                    accounts_list_animation.running = true
                                    show_hide_rotate_animation.running = true
                                    is_accounts_list_hide = false
                                }

                                internal.clear_list_view()
                                if(file_dialog_open == false) {
                                    file_dialog_open = true
                                    btn_icon_source = "../../img/icons/folder_open_icon.svg"
                                } else {
                                    file_dialog_open = false
                                    btn_icon_source = "../../img/icons/folder_icon.svg"
                                }
                                file_dialog.open()
                            }
                        }

                        RunBtn {
                            id: set_schedule
                            text: "Set schedule"
                            anchors.left: select_file_btn.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.leftMargin: 30
                            anchors.topMargin: 5
                            anchors.bottomMargin: 5


                            onClicked: {
                                if (datetime_schedule.enabled === false) {
                                    let current_datetime = new Date()
                                    datetime_schedule.text = `${current_datetime.getDate()}.${current_datetime.getMonth() + 1}.${current_datetime.getFullYear()} ${current_datetime.getHours()}:${current_datetime.getMinutes()}`
                                    datetime_schedule.opacity = 1
                                    datetime_schedule.enabled = true
                                    schedule_lbl.opacity = 1
                                    set_schedule.text = "Hide schedule settings"
                                } else {
                                    datetime_schedule.opacity = 0
                                    datetime_schedule.enabled = false
                                    schedule_lbl.opacity = 0
                                    set_schedule.text = "Set schedule"
                                }
                            }
                        }

                        DateTime {
                            id: datetime_schedule
                            opacity: 0
                            anchors.left: set_schedule.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.leftMargin: 15
                            anchors.bottomMargin: 5
                            anchors.topMargin: 5
                            enabled: false
                        }

                        Label {
                            id: schedule_lbl
                            height: 20
                            color: "#c3cbdd"
                            text: qsTr("Scheduled startup")
                            anchors.left: datetime_schedule.left
                            anchors.right: datetime_schedule.right
                            anchors.top: datetime_schedule.bottom
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            anchors.rightMargin: 0
                            anchors.leftMargin: 0
                            anchors.topMargin: 5
                            font.pointSize: 10
                            font.family: "Verdana"
                            opacity: 0
                        }
                    }

                    AccountToggle {
                        id: shuffle_wallets
                        objectName: `shuffle_wallets_${tab_name}`
                        switch_text_field: "Shuffle wallets"
                        visible: false
                        anchors.left: parent.left
                        anchors.top: file_content.bottom
                        anchors.topMargin: 20
                        anchors.leftMargin: 10
                    }

                    AccountToggle {
                        id: select_all
                        objectName: `select_all_${tab_name}`
                        switch_text_field: "Select all"
                        checked: false
                        visible: false
                        anchors.left: parent.left
                        anchors.top: shuffle_wallets.bottom
                        anchors.topMargin: 10
                        anchors.leftMargin: 10

                        onToggled: {
                            internal.change_packs_switch_status()
                        }
                    }

                    HideBtn {
                        id: show_hide_accounts_list_btn
                        width: 25
                        anchors.right: project_space.left
                        anchors.top: file_content.bottom
                        anchors.topMargin: 10
                        anchors.rightMargin: -25

                        RotationAnimator {
                            id: show_hide_rotate_animation
                            target: show_hide_accounts_list_btn
                            from: is_accounts_list_hide == false ? 0 : 180
                            to: is_accounts_list_hide == false ? 180 : 0
                            duration: 500
                        }

                        onClicked: {
                            show_hide_rotate_animation.running = true
                            internal.show_hide_packs_list_handler()
                            if (is_accounts_list_hide == false) {
                                is_accounts_list_hide = true
                            } else {
                                is_accounts_list_hide = false
                            }
                        }
                    }

                    ScrollView {
                        id: pack_list
                        width: 220
                        anchors.left: parent.left
                        anchors.top: select_all.bottom
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 10
                        anchors.leftMargin: 10
                        anchors.topMargin: 10
                        clip: true

                        Column {
                            id: pack_list_flickable_zone
                            spacing: 4
                            Repeater {
                                id: list_model
                                objectName: `list_model_${tab_name}`
                                model: []

                                delegate: AccountToggle {
                                    required property var modelData
                                    objectName: modelData
                                    switch_text_field: modelData
                                    checked: false
                                }
                            }
                        }
                    }

                    Rectangle {
                        id: project_space
                        color: "#2e2f30"
                        radius: 6
                        border.color: "#55aaff"
                        border.width: 2
                        anchors.left: pack_list.right
                        anchors.right: parent.right
                        anchors.top: show_hide_accounts_list_btn.bottom
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 10
                        anchors.leftMargin: 10
                        anchors.bottomMargin: 10
                        anchors.topMargin: 10

                        Flickable {
                            id: setting_space
                            width: 620
                            anchors.fill: parent
                            anchors.rightMargin: 5
                            anchors.leftMargin: 5
                            anchors.bottomMargin: 5
                            anchors.topMargin: 5
                            contentHeight: flickable_height
                            clip: true

                            Rectangle {
                                id: general_settings_space
                                width: 370
                                height: 78
                                color: "#2e2f30"
                                radius: 6
                                border.color: "#55aaff"
                                border.width: 2
                                anchors.left: parent.left
                                anchors.top: parent.top
                                anchors.topMargin: 10
                                anchors.leftMargin: 10

                                CustomTextField {
                                    id: max_gas_fee_field
                                    height: 28
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    horizontalAlignment: Text.AlignHCenter
                                    anchors.rightMargin: 100
                                    anchors.leftMargin: 100
                                    anchors.topMargin: 10
                                    readOnly: false
                                    validator: IntValidator{bottom: 0; top: 1000}

                                    onFocusChanged: {
                                        if (activeFocus === true) {
                                            selectAll()
                                        }

                                        if (max_gas_fee_field.text !== "") {
                                            if (Number(max_gas_fee_field.text) < 0) {
                                                max_gas_fee_field.is_valid = false
                                            } else {
                                                max_gas_fee_field.is_valid = true
                                            }
                                        }
                                    }
                                }

                                Label {
                                    id: max_gas_fee_lbl
                                    height: 20
                                    width: max_gas_fee_field.width
                                    text: "Max GAS fee"
                                    color: "#81848c"
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: max_gas_fee_field.left
                                    anchors.top: max_gas_fee_field.bottom
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 5
                                }
                            }

                            Rectangle {
                                id: input_space
                                width: 370
                                height: 116
                                color: "#2e2f30"
                                radius: 6
                                border.color: "#55aaff"
                                border.width: 2
                                anchors.left: parent.left
                                anchors.top: general_settings_space.bottom
                                anchors.leftMargin: 10
                                anchors.topMargin: 10

                                Row {
                                    id: networks_selector_row
                                    height: 48
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    anchors.rightMargin: 0
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0

                                    ChainSelector {
                                        id: source_network_cb
                                        width: 150
                                        model: source_networks
                                        height: 28
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10

                                        onCurrentTextChanged: {
                                            destination_network_cb.model = internal.networks_match[source_network_cb.currentText]
                                        }

                                    }

                                    ChainSelector {
                                        id: destination_network_cb
                                        width: 150
                                        model: []
                                        height: 28
                                        anchors.left: source_network_cb.right
                                        anchors.top: parent.top
                                        anchors.leftMargin: 50
                                        anchors.topMargin: 10
                                    }
                                }

                                Row {
                                    id: input_field_row
                                    height: 68
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: networks_selector_row.bottom
                                    anchors.rightMargin: 0
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0


                                    CustomTextField {
                                        id: input_min_field
                                        width: 150
                                        height: 28
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        readOnly: false

                                        onFocusChanged: {
                                            if (activeFocus === true) {
                                            selectAll()
                                            }
                                        }
                                    }

                                    Label {
                                        id: input_min_lbl
                                        height: 20
                                        width: input_min_field.width
                                        text: "Min amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: input_min_field.bottom
                                        anchors.left: input_min_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    CustomTextField {
                                        id: input_max_field
                                        width: 150
                                        height: 28
                                        anchors.left: input_min_field.right
                                        anchors.top: parent.top
                                        anchors.leftMargin: 50
                                        anchors.topMargin: 10
                                        readOnly: false
                                        
                                        onFocusChanged: {
                                            if (activeFocus === true) {
                                            selectAll()
                                            }
                                        }
                                    }

                                    Label {
                                        id: input_max_lbl
                                        height: 20
                                        width: input_max_field.width
                                        text: "Max amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: input_max_field.bottom
                                        anchors.left: input_max_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }
                                }
                            }

                            Rectangle {
                                id: time_setter_space
                                width: 370
                                height: 126
                                color: "#2e2f30"
                                radius: 6
                                border.color: "#55aaff"
                                border.width: 2
                                anchors.left: parent.left
                                anchors.top: input_space.bottom
                                anchors.leftMargin: 10
                                anchors.topMargin: 10

                                Rectangle {
                                    id: time_from_space
                                    width: parent.width / 2 - 15
                                    height: 68
                                    color: "#2e2f30"
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                    enabled: asap_toggle.checked ? false : true
                                    opacity: asap_toggle.checked ? 0.5 : 1

                                    Label {
                                        id: min_time_lbl
                                        height: 20
                                        color: "#c3cbdd"
                                        text: qsTr("Minimum time value")
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                        anchors.topMargin: 5
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        font.pointSize: 10
                                        font.family: "Verdana"
                                    }

                                    CustomTextField {
                                        id: time_from_field
                                        height: 28
                                        anchors.top: min_time_lbl.bottom
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        anchors.topMargin: 10
                                        width: parent.width - 20
                                        placeholderText: qsTr("00:00")
                                        readOnly: false
                                        inputMask: "00:00"

                                        ToolTip {
                                            id: time_from_tool_tip
                                            text: qsTr("Enter the minimum time to complete tasks in the format HH:MM (ex. 00:10)")
                                            delay: 500
                                            visible: time_from_field.hovered

                                            contentItem: Text {
                                                text: time_from_tool_tip.text
                                                font: time_from_tool_tip.font
                                                color: "#c3cbdd"
                                            }

                                            background: Rectangle {
                                                color: "#1b1b1c"
                                                border.width: 2
                                                border.color: "#cc0000"
                                                radius: 6
                                            }
                                        }
                                    }
                                }

                                Rectangle {
                                    id: time_to_space
                                    width: parent.width / 2 - 15
                                    height: 68
                                    color: "#2e2f30"
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    anchors.rightMargin: 10
                                    anchors.topMargin: 10
                                    enabled: asap_toggle.checked ? false : true
                                    opacity: asap_toggle.checked ? 0.5 : 1

                                    Label {
                                        id: max_time_lbl
                                        height: 20
                                        color: "#c3cbdd"
                                        text: qsTr("Maximum time value")
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                        anchors.topMargin: 5
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        font.pointSize: 10
                                        font.family: "Verdana"
                                    }

                                    CustomTextField {
                                        id: time_to_field
                                        height: 28
                                        anchors.top: max_time_lbl.bottom
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        anchors.topMargin: 10
                                        width: parent.width - 20
                                        placeholderText: qsTr("00:00")
                                        readOnly: false
                                        inputMask: "00:00"

                                        ToolTip {
                                            id: time_to_tool_tip
                                            text: qsTr("Enter the maximum time to complete tasks in the format HH:MM (ex. 00:10)")
                                            delay: 500
                                            visible: time_to_field.hovered

                                            contentItem: Text {
                                                text: time_to_tool_tip.text
                                                font: time_to_tool_tip.font
                                                color: "#c3cbdd"
                                            }

                                            background: Rectangle {
                                                color: "#1b1b1c"
                                                border.width: 2
                                                border.color: "#cc0000"
                                                radius: 6
                                            }
                                        }

                                        onFocusChanged: {
                                            if (time_from_field.text !== ":" && time_to_field.text !== ":"){
                                                backend.time_validator(time_from_field.text, time_to_field.text)
                                            }
                                        }
                                    }
                                }

                                AccountToggle {
                                    id: asap_toggle
                                    switch_text_field: qsTr("ASAP")
                                    width: parent.width / 4
                                    anchors.top: time_to_space.bottom
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    anchors.topMargin: 10
                                    checked: false
                                    switch_height: 15
                                    switch_width: 30
                                }
                            }

                            RunBtn {
                                id: run_btn
                                anchors.left: parent.left
                                anchors.right: general_settings_space.right
                                anchors.top: time_setter_space.bottom
                                anchors.leftMargin: 10
                                anchors.rightMargin: 0
                                anchors.topMargin: 10

                                onClicked: {
                                    let valid = internal.validation()
                                    if (valid === true) {
                                        internal.get_accounts_switch_status()
                                        let window_setting = {
                                            "datetime_schedule":{"enabled": datetime_schedule.enabled, "text": datetime_schedule.text},
                                            "max_gas_fee_field": {"enabled": max_gas_fee_field.enabled, "text": max_gas_fee_field.text},
                                            "input_min_field": {"enabled": input_min_field.enabled, "text": input_min_field.text},
                                            "input_max_field": {"enabled": input_max_field.enabled, "text": input_max_field.text},
                                            "source_network_cb": {"enabled": source_network_cb.enabled, "text": source_network_cb.currentText},
                                            "destination_network_cb": {"enabled": destination_network_cb.enabled, "text": destination_network_cb.currentText},
                                            "time_from_field": {"enabled": time_from_field.enabled, "text": time_from_field.text},
                                            "time_to_field": {"enabled": time_to_field.enabled, "text": time_to_field.text},
                                            "asap_toggle": {"enabled": asap_toggle.enabled, "checked": asap_toggle.checked}
                                        }
                                        internal.lock_ui()
                                        backend.run_project(window_setting, "Merkly", tab_name)
                                    }
                                }
                            }

                            RunBtn {
                                id: save_config_btn
                                text: "Save config"
                                anchors.right: run_btn.right
                                anchors.top: run_btn.bottom
                                anchors.rightMargin: 0
                                anchors.topMargin: 10

                                onClicked: {
                                    save_config_dialog.project_name = "Merkly"
                                    save_config_dialog.visible = true
                                }
                            }
                        }

                        Rectangle {
                            id: logging_space
                            color: "#2e2f30"
                            radius: 6
                            border.color: "#55aaff"
                            border.width: 2
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.rightMargin: 15
                            anchors.leftMargin: 650
                            anchors.bottomMargin: 15
                            anchors.topMargin: 15

                            ScrollView {
                                id: output_field_sv
                                anchors.fill: parent
                                clip: true

                                TextArea {
                                    id: output_field
                                    width: 990
                                    height: 858
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    objectName: tab_name
                                    font.pixelSize: 14
                                    font.family: "Verdana"
                                    textFormat: TextEdit.RichText
                                    readOnly: true
                                    wrapMode: Text.WordWrap
                                    anchors.topMargin: 0
                                    background: Rectangle {
                                        id: output_background
                                        color: "#2e2f30"
                                        border.color: "#55aaff"
                                        radius: 6
                                        border.width: 2
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
