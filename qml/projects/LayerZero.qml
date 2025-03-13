import QtQuick
import QtCore
import QtQuick.Window
import QtQuick.Controls 6.3
import QtQuick.Layouts 6.3
import QtQuick.Dialogs
import Qt.labs.settings 1.1
import "../controls"

Rectangle {
    id: layer_zero_window
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
                                                output_space.height + time_setter_space.height

    SaveConfigDialog {
        id: save_config_dialog
        visible: false

        onAccepted: {
            close()
            backend.save_config(save_config_dialog.project_name, layer_zero_window.settings_name, save_config_dialog.settings_name)
        }
    }

    Settings {
        id: layer_zero_settings
        fileName: `settings/Layer Zero/${settings_name}`

        property alias max_gas_fee_field: max_gas_fee_field.text
        property alias slippage_field: slippage_field.text
        property alias bridge_iteration_field: bridge_iteration_field.text
        property alias max_stargate_fee_field: max_stargate_fee_field.text
        property alias percent_to_bridge_field: percent_to_bridge_field.text

        property alias start_bridge_cb: start_bridge_cb.currentIndex
        property alias finish_bridge_cb: finish_bridge_cb.currentIndex

        property alias arbitrum_toggle: arbitrum_toggle.checked
        property alias arbitrum_toggle_enabled: arbitrum_toggle.enabled
        property alias arbitrum_toggle_opacity: arbitrum_toggle.opacity
        property alias arbitrum_icon_enabled: arbitrum_icon.enabled
        property alias arbitrum_icon_opacity: arbitrum_icon.opacity
        property alias optimism_toggle: optimism_toggle.checked
        property alias optimism_toggle_enabled: optimism_toggle.enabled
        property alias optimism_toggle_opacity: optimism_toggle.opacity
        property alias optimism_icon_enabled: optimism_icon.enabled
        property alias optimism_icon_opacity: optimism_icon.opacity
        property alias base_toggle: base_toggle.checked
        property alias base_toggle_enabled: base_toggle.enabled
        property alias base_toggle_opacity: base_toggle.opacity
        property alias base_icon_enabled: base_icon.enabled
        property alias base_icon_opacity: base_icon.opacity
        property alias linea_toggle: linea_toggle.checked
        property alias linea_toggle_enabled: linea_toggle.enabled
        property alias linea_toggle_opacity: linea_toggle.opacity
        property alias linea_icon_enabled: linea_icon.enabled
        property alias linea_icon_opacity: linea_icon.opacity
        property alias ethereum_toggle: ethereum_toggle.checked
        property alias ethereum_toggle_enabled: ethereum_toggle.enabled
        property alias ethereum_toggle_opacity: ethereum_toggle.opacity
        property alias ethereum_icon_enabled: ethereum_icon.enabled
        property alias ethereum_icon_opacity: ethereum_icon.opacity
        property alias avalanche_toggle: avalanche_toggle.checked
        property alias avalanche_toggle_enabled: avalanche_toggle.enabled
        property alias avalanche_toggle_opacity: avalanche_toggle.opacity
        property alias avalanche_icon_enabled: avalanche_icon.enabled
        property alias avalanche_icon_opacity: avalanche_icon.opacity
        property alias polygon_toggle: polygon_toggle.checked
        property alias polygon_toggle_enabled: polygon_toggle.enabled
        property alias polygon_toggle_opacity: polygon_toggle.opacity
        property alias polygon_icon_enabled: polygon_icon.enabled
        property alias polygon_icon_opacity: polygon_icon.opacity
        property alias bsc_toggle: bsc_toggle.checked
        property alias bsc_toggle_enabled: bsc_toggle.enabled
        property alias bsc_toggle_opacity: bsc_toggle.opacity
        property alias bsc_icon_enabled: bsc_icon.enabled
        property alias bsc_icon_opacity: bsc_icon.opacity
        property alias fantom_toggle: fantom_toggle.checked
        property alias fantom_toggle_enabled: fantom_toggle.enabled
        property alias fantom_toggle_opacity: fantom_toggle.opacity
        property alias fantom_icon_enabled: fantom_icon.enabled
        property alias fantom_icon_opacity: fantom_icon.opacity
        property alias kava_toggle: kava_toggle.checked
        property alias kava_toggle_enabled: kava_toggle.enabled
        property alias kava_toggle_opacity: kava_toggle.opacity
        property alias kava_icon_enabled: kava_icon.enabled
        property alias kava_icon_opacity: kava_icon.opacity

        property alias input_okx_to_aptos_toggle: input_okx_to_wallet_toggle.checked
        property alias input_balance_on_wallet_toggle: input_balance_on_wallet_toggle.checked
        property alias input_okx_to_aptos_toggle_enabled: input_okx_to_wallet_toggle.enabled
        property alias input_balance_on_wallet_toggle_enabled: input_balance_on_wallet_toggle.enabled
        property alias input_okx_to_aptos_toggle_opacity: input_okx_to_wallet_toggle.opacity
        property alias input_balance_on_wallet_toggle_opacity: input_balance_on_wallet_toggle.opacity
        property alias input_min_field: input_min_field.text
        property alias input_max_field: input_max_field.text
        property alias coin_selector_current_index: coin_selector.currentIndex

        property alias output_min_field: output_min_field.text
        property alias output_max_field: output_max_field.text
        property alias output_min_field_enabled: output_min_field.enabled
        property alias output_max_field_enabled: output_max_field.enabled
        property alias output_min_field_opacity: output_min_field.opacity
        property alias output_max_field_opacity: output_max_field.opacity
        property alias output_wallet_to_okx_toggle: output_wallet_to_okx_toggle.checked
        property alias output_coin_selector: output_coin_selector.currentText

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

    PropertyAnimation {
        id: accounts_list_animation
        target: pack_list
        property: "width"
        to: pack_list.width == 220 ? 0 : 220
        duration: 500
        easing.type: Easing.InOutQuint
    }

    DoubleValidator {
        id: percent_validator
        bottom: 0.0
        top: 100.0
        locale: "en_EN"
    }

    QtObject {
        id: internal

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

            if (slippage_field.text === "") {
                slippage_field.is_valid = false
                run_btn.enabled = false
                run_btn.opacity = 0.5
                return false
            } else {
                slippage_field.is_valid = true
                run_btn.enabled = true
                run_btn.opacity = 1
            }

            if (input_okx_to_wallet_toggle.checked === true) {
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
            }

            if (output_wallet_to_okx_toggle.checked === true) {
                if (output_min_field.text === "") {
                    output_min_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    output_min_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }

                if (output_max_field.text === "") {
                    output_max_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    output_max_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }
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
                        text: qsTr("AirDrop activities for Layer Zero")
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
                        source: "../../img/projects_logo/Layerzero.png"
                        anchors.leftMargin: 5
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        fillMode: Image.PreserveAspectFit
                    }

                    Label {
                        id: title_lbl
                        color: "#c3cbdd"
                        text: qsTr("Layer Zero")
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
                            placeholderText: qsTr("Select file with accounts info")

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
                                width: 600
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
                                    width: 108
                                    height: 28
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
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
                                                run_btn.enabled = false
                                                run_btn.opacity = 0.5
                                            } else {
                                                max_gas_fee_field.is_valid = true
                                                run_btn.enabled = true
                                                run_btn.opacity = 1
                                            }
                                        }
                                    }
                                }

                                Label {
                                    id: max_gas_fee_lbl
                                    height: 20
                                    width: 108
                                    text: "Max GAS fee"
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: parent.left
                                    anchors.top: max_gas_fee_field.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 5
                                }

                                CustomTextField {
                                    id: slippage_field
                                    width: 108
                                    height: 28
                                    anchors.left: max_gas_fee_field.right
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                    readOnly: false
                                    validator: DoubleValidator{bottom: 0; top: 100; locale: "en_EN"}

                                    onFocusChanged: {
                                        if (activeFocus === true) {
                                            selectAll()
                                        }

                                        if (slippage_field.text !== "") {
                                            if (Number(slippage_field.text) < 0 || Number(slippage_field.text) > 100) {
                                                slippage_field.is_valid = false
                                                run_btn.enabled = false
                                                run_btn.opacity = 0.5
                                            } else {
                                                slippage_field.is_valid = true
                                                run_btn.enabled = true
                                                run_btn.opacity = 1
                                            }
                                        }
                                    }
                                }

                                Label {
                                    id: slippage_lbl
                                    height: 20
                                    width: 108
                                    text: "Slippage, %"
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: max_gas_fee_lbl.right
                                    anchors.top: slippage_field.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 5
                                }

                                CustomTextField {
                                    id: bridge_iteration_field
                                    width: 108
                                    height: 28
                                    anchors.left: slippage_field.right
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                    readOnly: false
                                    validator: IntValidator{bottom: 0; top: 1000}

                                    onFocusChanged: {
                                        if (activeFocus === true) {
                                            selectAll()
                                        }

                                        if (bridge_iteration_field.text !== "") {
                                            if (Number(bridge_iteration_field.text) < 0) {
                                                bridge_iteration_field.is_valid = false
                                                run_btn.enabled = false
                                                run_btn.opacity = 0.5
                                            } else {
                                                bridge_iteration_field.is_valid = true
                                                run_btn.enabled = true
                                                run_btn.opacity = 1
                                            }
                                        }
                                    }
                                }

                                Label {
                                    id: bridge_iteration_lbl
                                    height: 20
                                    width: 108
                                    text: "Bridge iteration"
                                    wrapMode: Text.WordWrap
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: slippage_lbl.right
                                    anchors.top: bridge_iteration_field.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 5
                                }

                                CustomTextField {
                                    id: max_stargate_fee_field
                                    width: 108
                                    height: 28
                                    anchors.left: bridge_iteration_field.right
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                    readOnly: false
                                    validator: DoubleValidator{bottom: 0; top: 100; locale: "en_EN"}

                                    onFocusChanged: {
                                        if (activeFocus === true) {
                                            selectAll()
                                        }

                                        if (max_stargate_fee_field.text !== "") {
                                            if (Number(max_stargate_fee_field.text) < 0) {
                                                max_stargate_fee_field.is_valid = false
                                                run_btn.enabled = false
                                                run_btn.opacity = 0.5
                                            } else {
                                                max_stargate_fee_field.is_valid = true
                                                run_btn.enabled = true
                                                run_btn.opacity = 1
                                            }
                                        }
                                    }
                                }

                                Label {
                                    id: max_stargate_fee_lbl
                                    height: 20
                                    width: 108
                                    text: "Max Stargate fee"
                                    wrapMode: Text.WordWrap
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: bridge_iteration_lbl.right
                                    anchors.top: max_stargate_fee_field.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 5
                                }

                                CustomTextField {
                                    id: percent_to_bridge_field
                                    width: 108
                                    height: 28
                                    anchors.left: max_stargate_fee_field.right
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                    readOnly: false
                                    validator: DoubleValidator{bottom: 0; top: 100; locale: "en_EN"}

                                    onFocusChanged: {
                                        if (activeFocus === true) {
                                            selectAll()
                                        }

                                        if (max_stargate_fee_field.text !== "") {
                                            if (Number(max_stargate_fee_field.text) < 0) {
                                                max_stargate_fee_field.is_valid = false
                                                run_btn.enabled = false
                                                run_btn.opacity = 0.5
                                            } else {
                                                max_stargate_fee_field.is_valid = true
                                                run_btn.enabled = true
                                                run_btn.opacity = 1
                                            }
                                        }
                                    }
                                }

                                Label {
                                    id: percent_to_bridge_lbl
                                    height: 20
                                    width: 108
                                    text: "Amount to bridge, %"
                                    wrapMode: Text.WordWrap
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: max_stargate_fee_lbl.right
                                    anchors.top: percent_to_bridge_field.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 5
                                }
                            }

                            Rectangle {
                                id: input_space
                                width: 600
                                height: 300
                                color: "#2e2f30"
                                radius: 6
                                border.color: "#55aaff"
                                border.width: 2
                                anchors.left: parent.left
                                anchors.top: general_settings_space.bottom
                                anchors.leftMargin: 10
                                anchors.topMargin: 10

                                Label {
                                    id: start_network_lbl
                                    height: 28
                                    width: 40
                                    text: "Start"
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                }

                                ChainSelector {
                                    id: start_bridge_cb
                                    height: 28
                                    width: 150
                                    anchors.left: start_network_lbl.right
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                    model: [
                                        "Arbitrum",
                                        "Avalanche",
                                        "Optimism",
                                        "Polygon",
                                        "Ethereum",
                                        "Linea"
                                    ]

                                    onCurrentTextChanged: {
                                        if (start_bridge_cb.currentText === "Arbitrum" || start_bridge_cb.currentText === "Optimism" ||
                                                start_bridge_cb.currentText === "Ethereum" || start_bridge_cb.currentText === "Base" ||
                                                start_bridge_cb.currentText === "Linea") {
                                            coin_selector.model = ["USDT", "USDC", "ETH"]
                                        } else {
                                            coin_selector.model = ["USDT", "USDC"]
                                        }
                                    }
                                }

                                Label {
                                    id: finish_network_lbl
                                    height: 28
                                    width: 40
                                    text: "Finish"
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: start_bridge_cb.right
                                    anchors.top: parent.top
                                    anchors.leftMargin: 30
                                    anchors.topMargin: 10
                                }

                                ChainSelector {
                                    id: finish_bridge_cb
                                    height: 28
                                    width: 150
                                    anchors.left: finish_network_lbl.right
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                    model: [
                                        "Arbitrum",
                                        "Optimism",
                                        "Linea",
                                        "Base"
                                    ]
                                }

                                Label {
                                    id: route_lbl
                                    height: 28
                                    width: 40
                                    text: "Route"
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: parent.left
                                    anchors.top: start_network_lbl.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 40
                                }

                                Image {
                                    id: arbitrum_icon
                                    width: 20
                                    anchors.left: route_lbl.right
                                    anchors.top: start_network_lbl.bottom
                                    source: "../../img/networks_logo/arbitrum-arb-logo.svg"
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 40
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "Arbitrum" || finish_bridge_cb.currentText === "Arbitrum" ? false : true
                                    opacity: start_bridge_cb.currentText === "Arbitrum" || finish_bridge_cb.currentText === "Arbitrum" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: arbitrum_toggle
                                    objectName: "arbitrum_toggle"
                                    width: 100
                                    anchors.left: arbitrum_icon.right
                                    anchors.top: start_network_lbl.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 40
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "Arbitrum"
                                    checked: start_bridge_cb.currentText === "Arbitrum" || finish_bridge_cb.currentText === "Arbitrum" ? false : false
                                    enabled: start_bridge_cb.currentText === "Arbitrum" || finish_bridge_cb.currentText === "Arbitrum" ? false : true
                                    opacity: start_bridge_cb.currentText === "Arbitrum" || finish_bridge_cb.currentText === "Arbitrum" ? 0.5 : 1
                                }

                                Image {
                                    id: optimism_icon
                                    width: 20
                                    anchors.left: arbitrum_toggle.right
                                    anchors.top: start_network_lbl.bottom
                                    source: "../../img/networks_logo/optimism.svg"
                                    anchors.leftMargin: 40
                                    anchors.topMargin: 40
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "Optimism" || finish_bridge_cb.currentText === "Optimism" ? false : true
                                    opacity: start_bridge_cb.currentText === "Optimism" || finish_bridge_cb.currentText === "Optimism" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: optimism_toggle
                                    objectName: "optimism_toggle"
                                    width: 100
                                    anchors.left: optimism_icon.right
                                    anchors.top: start_network_lbl.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 40
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "Optimism"
                                    checked: start_bridge_cb.currentText === "Optimism" || finish_bridge_cb.currentText === "Optimism" ? false : false
                                    enabled: start_bridge_cb.currentText === "Optimism" || finish_bridge_cb.currentText === "Optimism" ? false : true
                                    opacity: start_bridge_cb.currentText === "Optimism" || finish_bridge_cb.currentText === "Optimism" ? 0.5 : 1
                                }

                                Image {
                                    id: base_icon
                                    width: 20
                                    anchors.left: optimism_toggle.right
                                    anchors.top: start_network_lbl.bottom
                                    source: "../../img/networks_logo/base.svg"
                                    anchors.leftMargin: 40
                                    anchors.topMargin: 40
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "Base" || finish_bridge_cb.currentText === "Base" ? false : true
                                    opacity: start_bridge_cb.currentText === "Base" || finish_bridge_cb.currentText === "Base" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: base_toggle
                                    objectName: "base_toggle"
                                    width: 100
                                    anchors.left: base_icon.right
                                    anchors.top: start_network_lbl.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 40
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "Base"
                                    checked: start_bridge_cb.currentText === "Base" || finish_bridge_cb.currentText === "Base" ? false : false
                                    enabled: start_bridge_cb.currentText === "Base" || finish_bridge_cb.currentText === "Base" ? false : true
                                    opacity: start_bridge_cb.currentText === "Base" || finish_bridge_cb.currentText === "Base" ? 0.5 : 1
                                }

                                Image {
                                    id: linea_icon
                                    width: 20
                                    anchors.left: route_lbl.right
                                    anchors.top: arbitrum_icon.bottom
                                    source: "../../img/networks_logo/linea.svg"
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 20
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "Linea" || finish_bridge_cb.currentText === "Linea" ? false : true
                                    opacity: start_bridge_cb.currentText === "Linea" || finish_bridge_cb.currentText === "Linea" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: linea_toggle
                                    objectName: "linea_toggle"
                                    width: 100
                                    anchors.left: linea_icon.right
                                    anchors.top: arbitrum_icon.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 20
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "Linea"
                                    checked: start_bridge_cb.currentText === "Linea" || finish_bridge_cb.currentText === "Linea" ? false : false
                                    enabled: start_bridge_cb.currentText === "Linea" || finish_bridge_cb.currentText === "Linea" || coin_selector.currentText === "USDT" || coin_selector.currentText === "USDC" ? false : true
                                    opacity: start_bridge_cb.currentText === "Linea" || finish_bridge_cb.currentText === "Linea" || coin_selector.currentText === "USDT" || coin_selector.currentText === "USDC" ? 0.5 : 1
                                }

                                Image {
                                    id: ethereum_icon
                                    width: 20
                                    anchors.left: linea_toggle.right
                                    anchors.top: arbitrum_icon.bottom
                                    source: "../../img/networks_logo/ethereum-eth-logo.svg"
                                    anchors.leftMargin: 40
                                    anchors.topMargin: 20
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "Ethereum" || finish_bridge_cb.currentText === "Ethereum" ? false : true
                                    opacity: start_bridge_cb.currentText === "Ethereum" || finish_bridge_cb.currentText === "Ethereum" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: ethereum_toggle
                                    objectName: "ethereum_toggle"
                                    width: 100
                                    anchors.left: ethereum_icon.right
                                    anchors.top: arbitrum_icon.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 20
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "Ethereum"
                                    checked: start_bridge_cb.currentText === "Ethereum" || finish_bridge_cb.currentText === "Ethereum" ? false : false
                                    enabled: start_bridge_cb.currentText === "Ethereum" || finish_bridge_cb.currentText === "Ethereum" ? false : true
                                    opacity: start_bridge_cb.currentText === "Ethereum" || finish_bridge_cb.currentText === "Ethereum" ? 0.5 : 1
                                }

                                Image {
                                    id: avalanche_icon
                                    width: 20
                                    anchors.left: ethereum_toggle.right
                                    anchors.top: arbitrum_icon.bottom
                                    source: "../../img/networks_logo/avalanche.svg"
                                    anchors.leftMargin: 40
                                    anchors.topMargin: 20
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "Avalanche" || finish_bridge_cb.currentText === "Avalanche" ? false : true
                                    opacity: start_bridge_cb.currentText === "Avalanche" || finish_bridge_cb.currentText === "Avalanche" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: avalanche_toggle
                                    objectName: "avalanche_toggle"
                                    width: 100
                                    anchors.left: avalanche_icon.right
                                    anchors.top: arbitrum_icon.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 20
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "Avalanche"
                                    checked: start_bridge_cb.currentText === "Avalanche" || finish_bridge_cb.currentText === "Avalanche" ? false : false
                                    enabled: start_bridge_cb.currentText === "Avalanche" || finish_bridge_cb.currentText === "Avalanche" ? false : true
                                    opacity: start_bridge_cb.currentText === "Avalanche" || finish_bridge_cb.currentText === "Avalanche" ? 0.5 : 1
                                }

                                Image {
                                    id: polygon_icon
                                    width: 20
                                    anchors.left: route_lbl.right
                                    anchors.top: linea_icon.bottom
                                    source: "../../img/networks_logo/polygon.svg"
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 20
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "Polygon" || finish_bridge_cb.currentText === "Polygon" ? false : true
                                    opacity: start_bridge_cb.currentText === "Polygon" || finish_bridge_cb.currentText === "Polygon" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: polygon_toggle
                                    objectName: "polygon_toggle"
                                    width: 100
                                    anchors.left: polygon_icon.right
                                    anchors.top: linea_icon.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 20
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "Polygon"
                                    checked: start_bridge_cb.currentText === "Polygon" || finish_bridge_cb.currentText === "Polygon" ? false : false
                                    enabled: start_bridge_cb.currentText === "Polygon" || finish_bridge_cb.currentText === "Polygon" ? false : true
                                    opacity: start_bridge_cb.currentText === "Polygon" || finish_bridge_cb.currentText === "Polygon" ? 0.5 : 1
                                }

                                Image {
                                    id: bsc_icon
                                    width: 20
                                    anchors.left: polygon_toggle.right
                                    anchors.top: linea_icon.bottom
                                    source: "../../img/networks_logo/bsc.svg"
                                    anchors.leftMargin: 40
                                    anchors.topMargin: 20
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "BSC" || finish_bridge_cb.currentText === "BSC" ? false : true
                                    opacity: start_bridge_cb.currentText === "BSC" || finish_bridge_cb.currentText === "BSC" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: bsc_toggle
                                    objectName: "bsc_toggle"
                                    width: 100
                                    anchors.left: bsc_icon.right
                                    anchors.top: linea_icon.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 20
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "BSC"
                                    checked: start_bridge_cb.currentText === "BSC" || finish_bridge_cb.currentText === "BSC" ? false : false
                                    enabled: start_bridge_cb.currentText === "BSC" || finish_bridge_cb.currentText === "BSC" ? false : true
                                    opacity: start_bridge_cb.currentText === "BSC" || finish_bridge_cb.currentText === "BSC" ? 0.5 : 1
                                }

                                Image {
                                    id: fantom_icon
                                    width: 20
                                    anchors.left: bsc_toggle.right
                                    anchors.top: linea_icon.bottom
                                    source: "../../img/networks_logo/fantom.svg"
                                    anchors.leftMargin: 40
                                    anchors.topMargin: 20
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "Fantom" || finish_bridge_cb.currentText === "Fantom" ? false : true
                                    opacity: start_bridge_cb.currentText === "Fantom" || finish_bridge_cb.currentText === "Fantom" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: fantom_toggle
                                    objectName: "fantom_toggle"
                                    width: 100
                                    anchors.left: fantom_icon.right
                                    anchors.top: linea_icon.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 20
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "Fantom"
                                    checked: start_bridge_cb.currentText === "Fantom" || finish_bridge_cb.currentText === "Fantom" ? false : false
                                    enabled: start_bridge_cb.currentText === "Fantom" || finish_bridge_cb.currentText === "Fantom" ? false : true
                                    opacity: start_bridge_cb.currentText === "Fantom" || finish_bridge_cb.currentText === "Fantom" ? 0.5 : 1
                                }

                                Image {
                                    id: kava_icon
                                    width: 20
                                    anchors.left: polygon_toggle.right
                                    anchors.top: bsc_icon.bottom
                                    source: "../../img/networks_logo/kava.svg"
                                    anchors.leftMargin: 40
                                    anchors.topMargin: 20
                                    fillMode: Image.PreserveAspectFit
                                    enabled: start_bridge_cb.currentText === "Kava" || finish_bridge_cb.currentText === "Kava" ? false : true
                                    opacity: start_bridge_cb.currentText === "Kava" || finish_bridge_cb.currentText === "Kava" ? 0.5 : 1
                                }

                                AccountToggle {
                                    id: kava_toggle
                                    objectName: "kava_toggle"
                                    width: 100
                                    anchors.left: kava_icon.right
                                    anchors.top: bsc_icon.bottom
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 20
                                    switch_height: 15
                                    switch_width: 30
                                    switch_text_field: "Kava"
                                    checked: start_bridge_cb.currentText === "Kava" || finish_bridge_cb.currentText === "Kava" ? false : false
                                    enabled: start_bridge_cb.currentText === "Kava" || finish_bridge_cb.currentText === "Kava" ? false : true
                                    opacity: start_bridge_cb.currentText === "Kava" || finish_bridge_cb.currentText === "Kava" ? 0.5 : 1
                                }

                                Row {
                                    id: input_amount_settings_row
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: kava_icon.bottom
                                    anchors.rightMargin: 0
                                    anchors.leftMargin: 0
                                    anchors.bottomMargin: 40

                                    AccountToggle {
                                        id: input_okx_to_wallet_toggle
                                        width: 190
                                        switch_text_field: "OKX to wallet"
                                        checked: false
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.topMargin: 10
                                        font.pointSize: 10
                                        font.family: "Verdana"
                                        anchors.leftMargin: 10
                                        switch_height: 15
                                        switch_width: 30

                                        onToggled: {
                                            if (input_okx_to_wallet_toggle.checked === true) {
                                                input_min_field.enabled = true
                                                input_max_field.enabled = true
                                                input_balance_on_wallet_toggle.enabled = false
                                                input_balance_on_wallet_toggle.opacity = 0.5
                                            } else {
                                                input_min_field.enabled = false
                                                input_max_field.enabled = false
                                                input_min_field.text = ""
                                                input_max_field.text = ""
                                                input_balance_on_wallet_toggle.enabled = true
                                                input_balance_on_wallet_toggle.opacity = 1
                                            }
                                        }
                                    }

                                    AccountToggle {
                                        id: input_balance_on_wallet_toggle
                                        width: 190
                                        switch_text_field: "Balance on wallet"
                                        checked: false
                                        anchors.left: parent.left
                                        anchors.top: input_okx_to_wallet_toggle.bottom
                                        anchors.topMargin: 10
                                        font.pointSize: 10
                                        font.family: "Verdana"
                                        anchors.leftMargin: 10
                                        switch_height: 15
                                        switch_width: 30

                                        onToggled: {
                                            if (input_balance_on_wallet_toggle.checked === true) {
                                                input_min_field.enabled = false
                                                input_max_field.enabled = false
                                                input_min_field.text = ""
                                                input_max_field.text = ""
                                                input_okx_to_wallet_toggle.enabled = false
                                                input_okx_to_wallet_toggle.opacity = 0.5
                                            } else {
                                                input_min_field.enabled = true
                                                input_max_field.enabled = true
                                                input_okx_to_wallet_toggle.enabled = true
                                                input_okx_to_wallet_toggle.opacity = 1
                                            }
                                        }
                                    }

                                    CustomTextField {
                                        id: input_min_field
                                        width: 90
                                        height: 28
                                        anchors.left: input_okx_to_wallet_toggle.right
                                        read_only: false
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        enabled: input_okx_to_wallet_toggle.checked
                                        opacity: input_okx_to_wallet_toggle.checked === true ? 1 : 0.5
                                        validator: DoubleValidator{bottom: 0; top: 10000; locale: "en_EN"}

                                        ToolTip {
                                            id: input_min_amount_tool_tip
                                            text: qsTr("Min value for purchase or withdrawal")
                                            delay: 500
                                            visible: input_min_field.hovered

                                            contentItem: Text {
                                                text: input_min_amount_tool_tip.text
                                                font: input_min_amount_tool_tip.font
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
                                            if (activeFocus === true) {
                                                selectAll()
                                            }
                                        }
                                    }

                                    Label {
                                        id: input_min_lbl
                                        height: 20
                                        width: 90
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
                                        width: 90
                                        height: 28
                                        anchors.left: input_min_field.right
                                        read_only: false
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        opacity: input_okx_to_wallet_toggle.checked === true ? 1 : 0.5
                                        enabled: input_okx_to_wallet_toggle.checked
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}

                                        ToolTip {
                                            id: input_max_amount_tool_tip
                                            text: qsTr("Max value for purchase or withdrawal")
                                            delay: 500
                                            visible: input_max_field.hovered

                                            contentItem: Text {
                                                text: input_max_amount_tool_tip.text
                                                font: input_max_amount_tool_tip.font
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
                                            if (activeFocus === true) {
                                                selectAll()
                                            }

                                            if (input_max_field.text !== "" && input_min_field.text !== "") {
                                                if (Number(input_max_field.text) < Number(input_min_field.text)) {
                                                    input_max_field.is_valid = false
                                                    input_min_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    input_max_field.is_valid = true
                                                    input_min_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: input_max_lbl
                                        height: 20
                                        width: 90
                                        text: "Max amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: input_max_field.bottom
                                        anchors.left: input_min_lbl.right
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 10
                                    }

                                    ChainSelector {
                                        id: coin_selector
                                        height: 28
                                        anchors.left: input_max_field.right
                                        anchors.right: parent.right
                                        anchors.top: parent.top
                                        anchors.rightMargin: 10
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        model: ["USDT", "USDC", "ETH"]
                                    }
                                }
                            }

                            Rectangle {
                                id: output_space
                                width: 600
                                height: 154
                                color: "#2e2f30"
                                radius: 6
                                border.color: "#55aaff"
                                border.width: 2
                                anchors.left: parent.left
                                anchors.top: input_space.bottom
                                clip: true
                                anchors.leftMargin: 10
                                anchors.topMargin: 10

                                Row {
                                    id: aptos_output_field_row
                                    height: 86
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0

                                    AccountToggle {
                                        id: output_wallet_to_okx_toggle
                                        width: 190
                                        anchors.left: parent.left
                                        anchors.top: output_min_lbl.bottom
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 20
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("Wallet to OKX")
                                        checked: false
                                        enabled: finish_bridge_cb.currentText === "Base" ? false : true
                                        opacity: finish_bridge_cb.currentText === "Base" ? 0.5 : 1

                                        onToggled: {
                                            if (output_wallet_to_okx_toggle.checked === false) {
                                                output_min_field.enabled = false
                                                output_max_field.enabled = false
                                                output_min_field.text = ""
                                                output_max_field.text = ""
                                            } else {
                                                output_min_field.enabled = true
                                                output_max_field.enabled = true
                                            }
                                        }
                                    }

                                    ChainSelector {
                                        id: output_coin_selector
                                        height: 28
                                        width: 150
                                        anchors.left: output_wallet_to_okx_toggle.right
                                        anchors.top: output_wallet_to_okx_toggle.top
                                        anchors.rightMargin: 10
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 0
                                        model: ["USDT", "USDC", "ETH"]
                                    }

                                    CustomTextField {
                                        id: output_min_field
                                        width: 285
                                        height: 28
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        readOnly: false
                                        validator: DoubleValidator {bottom: 0; top: 10000; locale: "en_EN"}
                                        enabled: output_wallet_to_okx_toggle.checked
                                        opacity: output_wallet_to_okx_toggle.checked === true ? 1 : 0.5

                                        onFocusChanged: {
                                            if (activeFocus === true) {
                                                selectAll()
                                            }
                                        }
                                    }

                                    Label {
                                        id: output_min_lbl
                                        height: 10
                                        width: 285
                                        text: "Min wallet balance"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: output_min_field.bottom
                                        anchors.left: output_min_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    CustomTextField {
                                        id: output_max_field
                                        width: 285
                                        height: 28
                                        anchors.left: output_min_field.right
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        readOnly: false
                                        validator: DoubleValidator {bottom: 0; top: 10000; locale: "en_EN"}
                                        enabled: output_wallet_to_okx_toggle.checked
                                        opacity: output_wallet_to_okx_toggle.checked === true ? 1 : 0.5

                                        onFocusChanged: {
                                            if (activeFocus === true) {
                                                selectAll()
                                            }

                                            if (output_min_field.text !== "" && output_max_field.text !== "") {
                                                if (Number(output_min_field.text) > Number(output_max_field.text)) {
                                                    output_min_field.is_valid = false
                                                    output_max_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    output_min_field.is_valid = true
                                                    output_max_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: output_max_lbl
                                        height: 10
                                        width: 285
                                        text: "Max wallet balance"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: output_max_field.bottom
                                        anchors.left: output_max_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }
                                }
                            }

                            Rectangle {
                                id: time_setter_space
                                width: 300
                                height: 126
                                color: "#2e2f30"
                                radius: 6
                                border.color: "#55aaff"
                                border.width: 2
                                anchors.left: parent.left
                                anchors.top: output_space.bottom
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
                                anchors.right: general_settings_space.right
                                anchors.top: output_space.bottom
                                anchors.rightMargin: 0
                                anchors.topMargin: 10

                                onClicked: {
                                    let valid = internal.validation()
                                    if (valid === true) {
                                        internal.get_accounts_switch_status()
                                        let window_setting = {
                                            "datetime_schedule":{"enabled": datetime_schedule.enabled, "text": datetime_schedule.text},
                                            "max_gas_fee_field": {"enabled": max_gas_fee_field.enabled, "text": max_gas_fee_field.text},
                                            "slippage_field": {"enabled": slippage_field.enabled, "text": slippage_field.text},
                                            "bridge_iteration_field": {"enabled": bridge_iteration_field.enabled, "text": bridge_iteration_field.text},
                                            "max_stargate_fee_field": {"enabled": max_stargate_fee_field.enabled, "text":max_stargate_fee_field.text},
                                            "percent_to_bridge_field": {"enabled": percent_to_bridge_field.enabled, "text":percent_to_bridge_field.text},
                                            "start_bridge_cb": {"enabled": start_bridge_cb.enabled, "text":start_bridge_cb.currentText},
                                            "finish_bridge_cb": {"enabled": finish_bridge_cb.enabled, "text":finish_bridge_cb.currentText},
                                            "arbitrum_toggle": {"enabled": arbitrum_toggle.enabled, "checked": arbitrum_toggle.checked},
                                            "optimism_toggle": {"enabled": optimism_toggle.enabled, "checked": optimism_toggle.checked},
                                            "base_toggle": {"enabled": base_toggle.enabled, "checked": base_toggle.checked},
                                            "linea_toggle": {"enabled": linea_toggle.enabled, "checked": linea_toggle.checked},
                                            "ethereum_toggle": {"enabled": ethereum_toggle.enabled, "checked": ethereum_toggle.checked},
                                            "avalanche_toggle": {"enabled": avalanche_toggle.enabled, "checked": avalanche_toggle.checked},
                                            "polygon_toggle": {"enabled": polygon_toggle.enabled, "checked": polygon_toggle.checked},
                                            "bsc_toggle": {"enabled": bsc_toggle.enabled, "checked": bsc_toggle.checked},
                                            "fantom_toggle": {"enabled": fantom_toggle.enabled, "checked": fantom_toggle.checked},
                                            "kava_toggle": {"enabled": kava_toggle.enabled, "checked": kava_toggle.checked},
                                            "input_okx_to_wallet_toggle": {"enabled": input_okx_to_wallet_toggle.enabled, "checked": input_okx_to_wallet_toggle.checked},
                                            "input_balance_on_wallet_toggle" : {"enabled": input_balance_on_wallet_toggle.enabled, "checked": input_balance_on_wallet_toggle.checked},
                                            "input_max_field": {"enabled": input_max_field.enabled, "text": input_max_field.text},
                                            "input_min_field": {"enabled": input_min_field.enabled, "text": input_min_field.text},
                                            "coin_selector": {"enabled": coin_selector.enabled, "text": coin_selector.currentText},
                                            "output_wallet_to_okx_toggle": {"enabled": output_wallet_to_okx_toggle.enabled, "checked": output_wallet_to_okx_toggle.checked},
                                            "output_min_field": {"enabled": output_min_field.enabled, "text": output_min_field.text},
                                            "output_max_field": {"enabled": output_max_field.enabled, "text": output_max_field.text},
                                            "output_coin_selector": {"enabled": output_coin_selector.enabled, "text": output_coin_selector.currentText},
                                            "time_from_field": {"enabled": time_from_field.enabled, "text": time_from_field.text},
                                            "time_to_field": {"enabled": time_to_field.enabled, "text": time_to_field.text},
                                            "asap_toggle": {"enabled": asap_toggle.enabled, "checked": asap_toggle.checked}
                                        }
                                        internal.lock_ui()
                                        backend.run_project(window_setting, "Layer Zero", tab_name)
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
                                    save_config_dialog.project_name = "Layer Zero"
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
