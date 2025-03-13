import QtQuick
import QtCore
import QtQuick.Window
import QtQuick.Controls 6.3
import QtQuick.Layouts 6.3
import QtQuick.Dialogs
import Qt.labs.settings 1.1
import "../controls"

Rectangle {
    id: aptos_window
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
                                                swap_space.height + pool_space.height + lending_space.height +
                                                output_space.height + time_setter_space.height

    SaveConfigDialog {
        id: save_config_dialog
        visible: false

        onAccepted: {
            close()
            backend.save_config(save_config_dialog.project_name, aptos_window.settings_name, save_config_dialog.settings_name)
        }
    }

    Settings {
        id: aptos_settings
        fileName: `settings/Aptos/${settings_name}`

        property alias slippage_field: slippage_field.text
        property alias swap_iteration_field: swap_iteration_field.text
        property alias pool_iteration_field: pool_iteration_field.text
        property alias lending_iteration_field: lending_iteration_field.text

        property alias input_okx_to_aptos_toggle: input_okx_to_aptos_bridge_toggle.checked
        property alias input_min_field: input_min_field.text
        property alias input_max_field: input_max_field.text
        property alias coin_selector_current_index: coin_selector.currentIndex

        property alias swap_enable_toggle: swap_enable_toggle.checked
        property alias one_of_all_toggle: one_of_all_toggle.checked
        property alias all_to_apt_toggle: all_to_apt_toggle.checked
        property alias one_of_all_toggle_opacity: one_of_all_toggle.opacity
        property alias all_to_apt_toggle_opacity: all_to_apt_toggle.opacity
        property alias swap_min_field: swap_min_field.text
        property alias swap_max_field: swap_max_field.text
        property alias swap_pancakeswap_toggle: swap_pancakeswap_toggle.checked
        property alias swap_liquidswap_toggle: swap_liquidswap_toggle.checked
        property alias swap_fields_row_enabled: swap_fields_row.enabled
        property alias swap_selector_row_enabled: swap_selector_row.enabled
        property alias swap_space_height: swap_space.height

        property alias pool_enable_toggle: pool_enable_toggle.checked
        property alias pool_min_add_field: pool_add_min_field.text
        property alias pool_max_add_field: pool_add_max_field.text
        property alias pool_min_remove_field: pool_remove_min_field.text
        property alias pool_max_remove_field: pool_remove_max_field.text
        property alias pool_pancake_swap_toggle: pool_pancakeswap_toggle.checked
        property alias pool_liquidswap_toggle: pool_liquidswap_toggle.checked
        property alias pool_fields_row_enabled: pool_fields_row.enabled
        property alias pool_selector_row_enabled: pool_selector_row.enabled
        property alias pool_space_height: pool_space.height

        property alias lending_enable_toggle: lending_enable_toggle.checked
        property alias lending_remove_all_toggle: lending_remove_all_toggle.checked
        property alias lending_remove_all_toggle_opacity: lending_remove_all_toggle.opacity
        property alias lending_min_add_field: lending_add_min_field.text
        property alias lending_max_add_field: lending_add_max_field.text
        property alias lending_min_remove_field: lending_remove_min_field.text
        property alias lending_max_remove_field: lending_remove_max_field.text
        property alias lending_min_remove_field_enabled: lending_remove_min_field.enabled
        property alias lending_max_remove_field_enabled: lending_remove_max_field.enabled
        property alias lending_min_remove_field_opacity: lending_remove_min_field.opacity
        property alias lending_max_remove_field_opacity: lending_remove_max_field.opacity
        property alias lending_aptin_toggle: lending_aptin_toggle.checked
        property alias lending_aries_toggle: lending_aries_toggle.checked
        property alias lending_abel_finance_toggle: lending_abel_finance_toggle.checked
        property alias lending_space_height: lending_space.height

        property alias output_min_field: output_min_field.text
        property alias output_max_field: output_max_field.text
        property alias output_aptos_to_okx_toggle: output_aptos_to_okx_toggle.checked
        property alias output_sell_apt: output_sell_apt_toggle.checked
        property alias sell_apt_enabled: output_sell_apt_toggle.enabled

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
        id: swap_animation
        target: swap_space
        property: "height"
        to: swap_space.height === 154 ? 48 : 154
        duration: 500
        easing.type: Easing.InOutQuint
    }

    PropertyAnimation {
        id: pool_animation
        target: pool_space
        property: "height"
        to: pool_space.height == 154 ? 48 : 154
        duration: 500
        easing.type: Easing.InOutQuint
    }

    PropertyAnimation {
        id: accounts_list_animation
        target: pack_list
        property: "width"
        to: pack_list.width == 220 ? 0 : 220
        duration: 500
        easing.type: Easing.InOutQuint
    }

    PropertyAnimation {
        id: lending_animation
        target: lending_space
        property: "height"
        to: lending_space.height == 164 ? 48 : 164
        duration: 500
        easing.type: Easing.InOutQuint
    }

    PropertyAnimation {
        id: lending_opacity_animation
        target: lending_remove_all_toggle
        property: "opacity"
        to: lending_space.height == 164 ? 0 : 100
        duration: 500
        easing.type: Easing.InQuart
    }

    DoubleValidator {
        id: percent_validator
        bottom: 0.0
        top: 100.0
        locale: "en_EN"
    }

    PropertyAnimation {
        id: swap_opacity_animation
        target: one_of_all_toggle
        property: "opacity"
        to: swap_space.height == 154 ? 0 : 100
        duration: 500
        easing.type: Easing.InQuart
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

            if (input_okx_to_aptos_bridge_toggle.checked === true) {
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

            if (swap_enable_toggle.checked === true) {
                if (swap_iteration_field.text === "") {
                    swap_iteration_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    swap_iteration_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }

                if (swap_min_field.text === "") {
                    swap_min_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    swap_min_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }

                if (swap_max_field.text === "") {
                    swap_max_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    swap_max_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }
            }

            if (pool_enable_toggle.checked === true) {
                if (pool_iteration_field.text === "") {
                    pool_iteration_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    pool_iteration_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }

                if (pool_add_min_field.text === "") {
                    pool_add_min_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    pool_add_min_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }

                if (pool_add_max_field.text === "") {
                    pool_add_max_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    pool_add_max_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }

                if (pool_remove_min_field.text === "") {
                    pool_remove_min_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    pool_remove_min_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }

                if (pool_remove_max_field.text === "") {
                    pool_remove_max_field.is_valid = false
                    run_btn.enabled = false
                    run_btn.opacity = 0.5
                    return false
                } else {
                    pool_remove_max_field.is_valid = true
                    run_btn.enabled = true
                    run_btn.opacity = 1
                }
            }

            if (output_aptos_to_okx_toggle.checked === true) {
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
                        text: qsTr("AirDrop activities for Aptos")
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
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.topMargin: 0

                    Image {
                        id: app_icon
                        width: 28
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        source: "../../img/projects_logo/aptos.svg"
                        anchors.leftMargin: 5
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        fillMode: Image.PreserveAspectFit
                    }

                    Label {
                        id: title_lbl
                        color: "#c3cbdd"
                        text: qsTr("Aptos")
                        anchors.left: app_icon.right
                        anchors.right: config_lbl.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        anchors.rightMargin: 0
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
                                    id: slippage_field
                                    width: 138
                                    height: 28
                                    anchors.left: parent.left
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
                                    width: slippage_field.width
                                    text: "Slippage, %"
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: slippage_field.left
                                    anchors.top: slippage_field.bottom
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 5
                                }

                                CustomTextField {
                                    id: swap_iteration_field
                                    width: 138
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

                                        if (swap_iteration_field.text !== "") {
                                            if (Number(swap_iteration_field.text) < 0) {
                                                swap_iteration_field.is_valid = false
                                                run_btn.enabled = false
                                                run_btn.opacity = 0.5
                                            } else {
                                                swap_iteration_field.is_valid = true
                                                run_btn.enabled = true
                                                run_btn.opacity = 1
                                            }
                                        }
                                    }
                                }

                                Label {
                                    id: swap_iteration_lbl
                                    height: 20
                                    width: 186
                                    text: "Swap iteration"
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: swap_iteration_field.left
                                    anchors.top: swap_iteration_field.bottom
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 5
                                }

                                CustomTextField {
                                    id: pool_iteration_field
                                    width: 138
                                    height: 28
                                    anchors.left: swap_iteration_field.right
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                    readOnly: false
                                    validator: IntValidator{bottom: 0; top: 1000}

                                    onFocusChanged: {
                                        if (activeFocus === true) {
                                            selectAll()
                                        }

                                        if (pool_iteration_field.text !== "") {
                                            if (Number(pool_iteration_field.text) < 0) {
                                                pool_iteration_field.is_valid = false
                                                run_btn.enabled = false
                                                run_btn.opacity = 0.5
                                            } else {
                                                pool_iteration_field.is_valid = true
                                                run_btn.enabled = true
                                                run_btn.opacity = 1
                                            }
                                        }
                                    }
                                }

                                Label {
                                    id: pool_iteration_lbl
                                    height: 20
                                    width: pool_iteration_field.width
                                    text: "Pool iteration"
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: pool_iteration_field.left
                                    anchors.top: pool_iteration_field.bottom
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 5
                                }

                                CustomTextField {
                                    id: lending_iteration_field
                                    width: 138
                                    height: 28
                                    anchors.left: pool_iteration_field.right
                                    anchors.top: parent.top
                                    anchors.leftMargin: 10
                                    anchors.topMargin: 10
                                    readOnly: false
                                    validator: IntValidator{bottom: 0; top: 1000}

                                    onFocusChanged: {
                                        if (activeFocus === true) {
                                            selectAll()
                                        }


                                        if (lending_iteration_field.text !== "") {
                                            if (Number(lending_iteration_field.text) < 0) {
                                                lending_iteration_field.is_valid = false
                                                run_btn.enabled = false
                                                run_btn.opacity = 0.5
                                            } else {
                                                lending_iteration_field.is_valid = true
                                                run_btn.enabled = true
                                                run_btn.opacity = 1
                                            }
                                        }
                                    }
                                }

                                Label {
                                    id: lending_iteration_lbl
                                    height: 20
                                    width: lending_iteration_field.width
                                    text: "Lending iteration"
                                    color: "#81848c"
                                    horizontalAlignment: "AlignHCenter"
                                    verticalAlignment: "AlignVCenter"
                                    anchors.left: lending_iteration_field.left
                                    anchors.top: lending_iteration_field.bottom
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 5
                                }
                            }

                            Rectangle {
                                id: input_space
                                width: 600
                                height: 78
                                color: "#2e2f30"
                                radius: 6
                                border.color: "#55aaff"
                                border.width: 2
                                anchors.left: parent.left
                                anchors.top: general_settings_space.bottom
                                anchors.leftMargin: 10
                                anchors.topMargin: 10

                                Row {
                                    id: input_amount_settings_row
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    anchors.rightMargin: 0
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0

                                    AccountToggle {
                                        id: input_okx_to_aptos_bridge_toggle
                                        width: 190
                                        switch_text_field: qsTr("OKX to Aptos")
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
                                            if (input_okx_to_aptos_bridge_toggle.checked === true) {
                                                input_min_field.enabled = true
                                                input_max_field.enabled = true
                                            } else {
                                                input_min_field.enabled = false
                                                input_max_field.enabled = false
                                                input_min_field.text = ""
                                                input_max_field.text = ""
                                            }
                                        }
                                    }

                                    CustomTextField {
                                        id: input_min_field
                                        width: 90
                                        height: 28
                                        anchors.left: input_okx_to_aptos_bridge_toggle.right
                                        read_only: false
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        enabled: input_okx_to_aptos_bridge_toggle.checked
                                        opacity: input_okx_to_aptos_bridge_toggle.checked === true ? 1 : 0.5
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
                                        opacity: input_okx_to_aptos_bridge_toggle.checked === true ? 1 : 0.5
                                        enabled: input_okx_to_aptos_bridge_toggle.checked
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
                                        model: ["USDT", "USDC", "APT"]
                                    }
                                }
                            }

                            Rectangle {
                                id: swap_space
                                width: 600
                                height: 48
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
                                    id: swap_settings_row
                                    height: 48
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0

                                    AccountToggle {
                                        id: swap_enable_toggle
                                        width: 180
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("Swap enable")
                                        checked: false

                                        onToggled: {
                                            swap_animation.running = true
                                            swap_opacity_animation.running = true

                                            if (swap_enable_toggle.checked === false) {
                                                one_of_all_toggle.enabled = false
                                                one_of_all_toggle.checked = false
                                                all_to_apt_toggle.enabled = false
                                                all_to_apt_toggle.checked = false

                                                swap_fields_row.enabled = false
                                                swap_min_field.text = qsTr("")
                                                swap_max_field.text = qsTr("")

                                                swap_selector_row.enabled = false

                                                swap_pancakeswap_toggle.checked = false
                                                swap_liquidswap_toggle.checked = false

                                            } else {
                                                one_of_all_toggle.enabled = true
                                                all_to_apt_toggle.enabled = true
                                                swap_fields_row.enabled = true
                                                swap_selector_row.enabled = true
                                            }
                                        }
                                    }

                                    AccountToggle {
                                        id: one_of_all_toggle
                                        width: 180
                                        anchors.left: swap_enable_toggle.right
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("One of all")
                                        checked: false
                                        enabled: false
                                        opacity: 0
                                    }

                                    AccountToggle {
                                        id: all_to_apt_toggle
                                        width: 180
                                        anchors.left: one_of_all_toggle.right
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("All to APT")
                                        checked: false
                                        enabled: false
                                        opacity: swap_enable_toggle.checked === true ? 1 : 0
                                    }
                                }

                                Row {
                                    id: swap_fields_row
                                    height: 58
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: swap_settings_row.bottom
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0
                                    opacity: swap_enable_toggle.checked === true ? 1 : 0.5
                                    enabled: false

                                    CustomTextField {
                                        id: swap_min_field
                                        width: 275
                                        height: 28
                                        readOnly: false
                                        enabled: swap_enable_toggle.checked
                                        opacity: swap_enable_toggle.checked ? 1 : 0.5
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}

                                        onFocusChanged: {
                                            if (activeFocus === true) {
                                                selectAll()
                                            }

                                            if (swap_min_field.text !== "") {
                                                if (Number(swap_min_field.text) < 0) {
                                                    swap_min_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    swap_min_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: swap_min_lbl
                                        height: 10
                                        width: 275
                                        text: "Min amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: swap_min_field.bottom
                                        anchors.left: swap_min_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    CustomTextField {
                                        id: swap_max_field
                                        width: 275
                                        height: 28
                                        readOnly: false
                                        enabled: swap_enable_toggle.checked
                                        opacity: swap_enable_toggle.checked ? 1 : 0.5
                                        anchors.left: swap_min_field.right
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}

                                        onFocusChanged: {
                                            if (activeFocus === true) {
                                                selectAll()
                                            }

                                            if (swap_max_field.text !== "" && swap_min_field.text !== "") {
                                                if (Number(swap_min_field.text) > Number(swap_max_field.text)) {
                                                    swap_min_field.is_valid = false
                                                    swap_max_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    swap_min_field.is_valid = true
                                                    swap_max_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: swap_max_lbl
                                        height: 10
                                        width: 275
                                        text: "Max amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: swap_max_field.bottom
                                        anchors.left: swap_max_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }
                                }

                                Row {
                                    id: swap_selector_row
                                    height: 48
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: swap_fields_row.bottom
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0
                                    opacity: swap_enable_toggle.checked === true ? 1 : 0.5
                                    enabled: false

                                    AccountToggle {
                                        id: swap_pancakeswap_toggle
                                        width: 130
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("PancakeSwap")
                                        checked: false
                                    }

                                    AccountToggle {
                                        id: swap_liquidswap_toggle
                                        width: 130
                                        anchors.left: swap_pancakeswap_toggle.right
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("LiquidSwap")
                                        checked: false
                                    }
                                }
                            }

                            Rectangle {
                                id: pool_space
                                width: 600
                                height: 48
                                color: "#2e2f30"
                                radius: 6
                                border.color: "#55aaff"
                                border.width: 2
                                anchors.left: parent.left
                                anchors.top: swap_space.bottom
                                clip: true
                                anchors.leftMargin: 10
                                anchors.topMargin: 10

                                Row {
                                    id: pool_settings_row
                                    height: 48
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0

                                    AccountToggle {
                                        id: pool_enable_toggle
                                        width: 180
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("Pool enable")
                                        checked: false

                                        onToggled: {
                                            pool_animation.running = true
                                            if (pool_enable_toggle.checked === false) {
                                                pool_add_min_field.text = qsTr("")
                                                pool_add_max_field.text = qsTr("")
                                                pool_remove_min_field.text = qsTr("")
                                                pool_remove_max_field.text = qsTr("")
                                                pool_selector_row.enabled = false
                                                pool_pancakeswap_toggle.checked = false
                                                pool_liquidswap_toggle.checked = false

                                            } else {
                                                pool_fields_row.enabled = true
                                                pool_selector_row.enabled = true
                                            }
                                        }
                                    }
                                }

                                Row {
                                    id: pool_fields_row
                                    height: 58
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: pool_settings_row.bottom
                                    clip: true
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0
                                    enabled: false

                                    CustomTextField {
                                        id: pool_add_min_field
                                        width: 132
                                        height: 28
                                        readOnly: false
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}

                                        ToolTip {
                                            id: pool_add_min_field_tooltip
                                            text: qsTr("Enter min amount to add in liquidity pool")
                                            delay: 500
                                            visible: pool_add_min_field.hovered

                                            contentItem: Text {
                                                text: pool_add_min_field_tooltip.text
                                                font: pool_add_min_field_tooltip.font
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

                                            if (pool_add_min_field.text !== "") {
                                                if (Number(pool_add_min_field.text) < 0) {
                                                    pool_add_min_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    pool_add_min_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: pool_add_min_lbl
                                        height: 10
                                        width: 132
                                        text: "Min add amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: pool_add_min_field.bottom
                                        anchors.left: pool_add_min_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    CustomTextField {
                                        id: pool_add_max_field
                                        width: 132
                                        height: 28
                                        readOnly: false
                                        anchors.left: pool_add_min_field.right
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}

                                        ToolTip {
                                            id: pool_add_max_field_tooltip
                                            text: qsTr("Enter max amount to add in liquidity pool")
                                            delay: 500
                                            visible: pool_add_max_field.hovered

                                            contentItem: Text {
                                                text: pool_add_max_field_tooltip.text
                                                font: pool_add_max_field_tooltip.font
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

                                            if (pool_add_max_field.text !== "" && pool_add_min_field.text !== "") {
                                                if (Number(pool_add_min_field.text) > Number(pool_add_max_field.text)) {
                                                    pool_add_min_field.is_valid = false
                                                    pool_add_max_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    pool_add_min_field.is_valid = true
                                                    pool_add_max_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: pool_add_max_lbl
                                        height: 10
                                        width: 132
                                        text: "Max add amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: pool_add_max_field.bottom
                                        anchors.left: pool_add_max_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    CustomTextField {
                                        id: pool_remove_min_field
                                        width: 133
                                        height: 28
                                        readOnly: false
                                        anchors.left: pool_add_max_field.right
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}

                                        ToolTip {
                                            id: pool_remove_min_field_tooltip
                                            text: qsTr("Enter min amount to remove from liquidity pool")
                                            delay: 500
                                            visible: pool_remove_min_field.hovered

                                            contentItem: Text {
                                                text: pool_remove_min_field_tooltip.text
                                                font: pool_remove_min_field_tooltip.font
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

                                            if (pool_add_min_field.text !== "") {
                                                if (Number(pool_add_min_field.text) < 0) {
                                                    pool_add_min_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    pool_add_min_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: pool_remove_min_lbl
                                        height: 10
                                        width: 133
                                        text: "Min remove amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: pool_remove_min_field.bottom
                                        anchors.left: pool_remove_min_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    CustomTextField {
                                        id: pool_remove_max_field
                                        width: 132
                                        height: 28
                                        readOnly: false
                                        anchors.left: pool_remove_min_field.right
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}

                                        ToolTip {
                                            id: pool_remove_max_field_tooltip
                                            text: qsTr("Enter min amount to remove from liquidity pool")
                                            delay: 500
                                            visible: pool_remove_max_field.hovered

                                            contentItem: Text {
                                                text: pool_remove_max_field_tooltip.text
                                                font: pool_remove_max_field_tooltip.font
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

                                            if (pool_add_max_field.text !== "" && pool_add_min_field.text !== "") {
                                                if (Number(pool_add_min_field.text) > Number(pool_add_max_field.text)) {
                                                    pool_add_min_field.is_valid = false
                                                    pool_add_max_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    pool_add_min_field.is_valid = true
                                                    pool_add_max_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: pool_remove_max_lbl
                                        height: 10
                                        width: 133
                                        text: "Max remove amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: pool_remove_max_field.bottom
                                        anchors.left: pool_remove_max_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }
                                }

                                Row {
                                    id: pool_selector_row
                                    height: 48
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: pool_fields_row.bottom
                                    clip: true
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0
                                    enabled: false

                                    AccountToggle {
                                        id: pool_pancakeswap_toggle
                                        width: 130
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("PancakeSwap")
                                        checked: false
                                    }

                                    AccountToggle {
                                        id: pool_liquidswap_toggle
                                        width: 130
                                        anchors.left: pool_pancakeswap_toggle.right
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("LiquidSwap")
                                        checked: false
                                    }
                                }
                            }

                            Rectangle {
                                id: lending_space
                                width: 600
                                height: 48
                                color: "#2e2f30"
                                radius: 6
                                border.color: "#55aaff"
                                border.width: 2
                                anchors.left: parent.left
                                anchors.top: pool_space.bottom
                                anchors.topMargin: 10
                                anchors.leftMargin: 10

                                Row {
                                    id: lending_settings_row
                                    height: 48
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0

                                    AccountToggle {
                                        id: lending_enable_toggle
                                        width: 180
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("Lending enable")
                                        checked: false

                                        onToggled: {
                                            lending_animation.running = true
                                            lending_opacity_animation.running = true

                                            if (lending_enable_toggle.checked === false) {
                                                lending_add_min_field.text = qsTr("")
                                                lending_add_max_field.text = qsTr("")
                                                lending_remove_min_field.text = qsTr("")
                                                lending_remove_max_field.text = qsTr("")
                                                lending_remove_all_toggle.checked = false
                                                lending_aptin_toggle.checked = false
                                                lending_aries_toggle.checked = false
                                            }
                                        }
                                    }

                                    AccountToggle {
                                        id: lending_remove_all_toggle
                                        width: 180
                                        anchors.right: parent.right
                                        anchors.top: parent.top
                                        anchors.rightMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("Remove all")
                                        checked: false
                                        enabled: lending_enable_toggle.checked
                                        opacity: 0

                                        onToggled: {
                                            if (lending_remove_all_toggle.checked === true) {
                                                lending_remove_min_field.text = qsTr("")
                                                lending_remove_max_field.text = qsTr("")
                                            }
                                        }
                                    }
                                }

                                Row {
                                    id: lending_fields_row
                                    height: 68
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: lending_settings_row.bottom
                                    anchors.topMargin: 0
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    opacity: lending_enable_toggle.checked === true ? 1 : 0.5
                                    enabled: lending_enable_toggle.checked

                                    CustomTextField {
                                        id: lending_add_min_field
                                        width: 132
                                        height: 28
                                        readOnly: false
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}

                                        ToolTip {
                                            id: lending_add_min_field_tooltip
                                            text: qsTr("Enter min amount to add in lending")
                                            delay: 500
                                            visible: lending_add_min_field.hovered

                                            contentItem: Text {
                                                text: lending_add_min_field_tooltip.text
                                                font: lending_add_min_field_tooltip.font
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
                                        id: lending_add_min_lbl
                                        height: 10
                                        width: 132
                                        text: "Min add amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: lending_add_min_field.bottom
                                        anchors.left: lending_add_min_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    CustomTextField {
                                        id: lending_add_max_field
                                        width: 132
                                        height: 28
                                        readOnly: false
                                        anchors.left: lending_add_min_field.right
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}

                                        ToolTip {
                                            id: lending_add_max_tooltip
                                            text: qsTr("Enter max amount to add in lending")
                                            delay: 500
                                            visible: lending_add_max_field.hovered

                                            contentItem: Text {
                                                text: lending_add_max_tooltip.text
                                                font: lending_add_max_tooltip.font
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

                                            if (lending_add_max_field.text !== "" && lending_add_min_field.text !== "") {
                                                if (Number(lending_add_min_field.text) > Number(lending_add_max_field.text)) {
                                                    lending_add_min_field.is_valid = false
                                                    lending_add_max_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    lending_add_min_field.is_valid = true
                                                    lending_add_max_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: lending_add_max_lbl
                                        height: 10
                                        width: 132
                                        text: "Max add amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: lending_add_max_field.bottom
                                        anchors.left: lending_add_max_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    CustomTextField {
                                        id: lending_remove_min_field
                                        width: 133
                                        height: 28
                                        readOnly: false
                                        anchors.left: lending_add_max_field.right
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}
                                        enabled: lending_remove_all_toggle.checked === true ? false : true
                                        opacity: lending_remove_all_toggle.checked === true ? 0.5 : 1

                                        ToolTip {
                                            id: lending_remove_min_tooltip
                                            text: qsTr("Enter min amount to remove from lending")
                                            delay: 500
                                            visible: lending_remove_min_field.hovered

                                            contentItem: Text {
                                                text: lending_remove_min_tooltip.text
                                                font: lending_remove_min_tooltip.font
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
                                        id: lending_remove_min_lbl
                                        height: 10
                                        width: 133
                                        text: "Min remove amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: lending_remove_min_field.bottom
                                        anchors.left: lending_remove_min_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    CustomTextField {
                                        id: lending_remove_max_field
                                        width: 132
                                        height: 28
                                        readOnly: false
                                        anchors.left: lending_remove_min_field.right
                                        anchors.top: parent.top
                                        horizontalAlignment: Text.AlignHCenter
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        validator: DoubleValidator{bottom: 0; top: 100000; locale: "en_EN"}
                                        enabled: lending_remove_all_toggle.checked === true ? false : true
                                        opacity: lending_remove_all_toggle.checked === true ? 0.5 : 1

                                        ToolTip {
                                            id: lending_remove_max_tooltip
                                            text: qsTr("Enter min amount to remove from lending")
                                            delay: 500
                                            visible: lending_remove_max_field.hovered

                                            contentItem: Text {
                                                text: lending_remove_max_tooltip.text
                                                font: lending_remove_max_tooltip.font
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

                                            if (lending_remove_max_field.text !== "" && lending_remove_min_field.text !== "") {
                                                if (Number(lending_remove_min_field.text) > Number(lending_remove_max_field.text)) {
                                                    lending_remove_min_field.is_valid = false
                                                    lending_remove_max_field.is_valid = false
                                                    run_btn.enabled = false
                                                    run_btn.opacity = 0.5
                                                } else {
                                                    lending_remove_min_field.is_valid = true
                                                    lending_remove_max_field.is_valid = true
                                                    run_btn.enabled = true
                                                    run_btn.opacity = 1
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: lending_remove_max_lbl
                                        height: 10
                                        width: 132
                                        text: "Max remove amount"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: lending_remove_max_field.bottom
                                        anchors.left: lending_remove_max_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }
                                }

                                Row {
                                    id: lending_selector_row
                                    height: 48
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: lending_fields_row.bottom
                                    anchors.rightMargin: 10
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0
                                    opacity: lending_enable_toggle.checked === true ? 1 : 0.5
                                    enabled: lending_enable_toggle.checked

                                    AccountToggle {
                                        id: lending_aptin_toggle
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: "Aptin"
                                        checked: false
                                    }

                                    AccountToggle {
                                        id: lending_aries_toggle
                                        anchors.left: lending_aptin_toggle.right
                                        anchors.top: parent.top
                                        anchors.leftMargin: 50
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: "Aries"
                                        checked: false
                                    }

                                    AccountToggle {
                                        id: lending_abel_finance_toggle
                                        anchors.left: lending_aries_toggle.right
                                        anchors.top: parent.top
                                        anchors.leftMargin: 50
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: "Abel Finance"
                                        checked: false
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
                                anchors.top: lending_space.bottom
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
                                        id: output_aptos_to_okx_toggle
                                        width: 190
                                        anchors.left: parent.left
                                        anchors.top: output_min_lbl.bottom
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 20
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("Aptos to OKX")
                                        checked: false

                                        onToggled: {
                                            if (output_aptos_to_okx_toggle.checked === false) {
                                                output_min_field.enabled = false
                                                output_max_field.enabled = false
                                                output_sell_apt_toggle.enabled = false
                                                output_sell_apt_toggle.checked = false
                                                output_min_field.text = ""
                                                output_max_field.text = ""
                                            } else {
                                                output_min_field.enabled = true
                                                output_max_field.enabled = true
                                                output_sell_apt_toggle.enabled = true
                                            }
                                        }
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
                                        enabled: output_aptos_to_okx_toggle.checked
                                        opacity: output_aptos_to_okx_toggle.checked === true ? 1 : 0.5

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
                                        text: "Min wallet balance in APT"
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
                                        enabled: output_aptos_to_okx_toggle.checked
                                        opacity: output_aptos_to_okx_toggle.checked === true ? 1 : 0.5

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
                                        text: "Max wallet balance in APT"
                                        color: "#81848c"
                                        horizontalAlignment: "AlignHCenter"
                                        verticalAlignment: "AlignVCenter"
                                        anchors.top: output_max_field.bottom
                                        anchors.left: output_max_field.left
                                        anchors.topMargin: 5
                                        anchors.leftMargin: 0
                                    }

                                    AccountToggle {
                                        id: output_sell_apt_toggle
                                        width: 180
                                        anchors.left: parent.left
                                        anchors.top: output_aptos_to_okx_toggle.bottom
                                        anchors.leftMargin: 10
                                        anchors.topMargin: 10
                                        switch_height: 15
                                        switch_width: 30
                                        switch_text_field: qsTr("Sell APT on OKX")
                                        checked: false
                                        enabled: output_aptos_to_okx_toggle.checked
                                        opacity: output_sell_apt_toggle.enabled === true ? 1 : 0.5
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
                                            "slippage_field": {"enabled": slippage_field.enabled, "text": slippage_field.text},
                                            "swap_iteration_field": {"enabled": swap_iteration_field.enabled, "text": swap_iteration_field.text},
                                            "pool_iteration_field": {"enabled": pool_iteration_field.enabled, "text":pool_iteration_field.text},
                                            "lending_iteration_field": {"enabled": lending_iteration_field.enabled, "text": lending_iteration_field.text},
                                            "input_okx_to_aptos_bridge_toggle": {"enabled": input_okx_to_aptos_bridge_toggle.enabled, "checked": input_okx_to_aptos_bridge_toggle.checked},
                                            "input_max_field": {"enabled": input_max_field.enabled, "text": input_max_field.text},
                                            "input_min_field": {"enabled": input_min_field.enabled, "text": input_min_field.text},
                                            "coin_selector": {"enabled": coin_selector.enabled, "text": coin_selector.currentText},
                                            "swap_enable_toggle": {"enabled": swap_enable_toggle.enabled, "checked": swap_enable_toggle.checked},
                                            "swap_min_field": {"enabled": swap_min_field.enabled, "text": swap_min_field.text},
                                            "swap_max_field": {"enabled": swap_max_field.enabled, "text": swap_max_field.text},
                                            "swap_pancakeswap_toggle": {"enabled": swap_pancakeswap_toggle.enabled, "checked": swap_pancakeswap_toggle.checked},
                                            "swap_liquidswap_toggle": {"enabled": swap_liquidswap_toggle.enabled, "checked": swap_liquidswap_toggle.checked},
                                            "one_of_all_toggle": {"enabled": one_of_all_toggle.enabled, "checked": one_of_all_toggle.checked},
                                            "all_to_apt_toggle": {"enabled": all_to_apt_toggle.enabled, "checked": all_to_apt_toggle.checked},
                                            "pool_enable_toggle": {"enabled": pool_enable_toggle.enabled, "checked": pool_enable_toggle.checked},
                                            "pool_pancakeswap_toggle": {"enabled": pool_pancakeswap_toggle.enabled, "checked": pool_pancakeswap_toggle.checked},
                                            "pool_liquidswap_toggle": {"enabled": pool_liquidswap_toggle.enabled, "checked": pool_liquidswap_toggle.checked},
                                            "pool_add_min_field": {"enabled": pool_add_min_field.enabled, "text": pool_add_min_field.text},
                                            "pool_add_max_field": {"enabled": pool_add_max_field.enabled, "text": pool_add_max_field.text},
                                            "pool_remove_min_field": {"enabled": pool_remove_min_field.enabled, "text": pool_remove_min_field.text},
                                            "pool_remove_max_field": {"enabled": pool_remove_max_field.enabled, "text": pool_remove_max_field.text},
                                            "lending_enable_toggle": {"enabled": lending_enable_toggle.enabled, "checked": lending_enable_toggle.checked},
                                            "lending_remove_all_toggle": {"enabled": lending_remove_all_toggle.enabled, "checked": lending_remove_all_toggle.checked},
                                            "lending_add_min_field": {"enabled": lending_add_min_field.enabled, "text": lending_add_min_field.text},
                                            "lending_add_max_field": {"enabled": lending_add_max_field.enabled, "text": lending_add_max_field.text},
                                            "lending_remove_min_field": {"enabled": lending_remove_min_field.enabled, "text": lending_remove_min_field.text},
                                            "lending_remove_max_field": {"enabled": lending_remove_max_field.enabled, "text": lending_remove_max_field.text},
                                            "lending_aptin_toggle": {"enabled": lending_aptin_toggle.enabled, "checked": lending_aptin_toggle.checked},
                                            "lending_aries_toggle": {"enabled": lending_aries_toggle.enabled, "checked": lending_aries_toggle.checked},
                                            "lending_abel_finance_toggle": {"enabled": lending_abel_finance_toggle.enabled, "checked": lending_abel_finance_toggle.checked},
                                            "output_aptos_to_okx_toggle": {"enabled": output_aptos_to_okx_toggle.enabled, "checked": output_aptos_to_okx_toggle.checked},
                                            "output_min_field": {"enabled": output_min_field.enabled, "text": output_min_field.text},
                                            "output_max_field": {"enabled": output_max_field.enabled, "text": output_max_field.text},
                                            "output_sell_apt_toggle": {"enabled": output_sell_apt_toggle.enabled, "checked": output_sell_apt_toggle.checked},
                                            "time_from_field": {"enabled": time_from_field.enabled, "text": time_from_field.text},
                                            "time_to_field": {"enabled": time_to_field.enabled, "text": time_to_field.text},
                                            "asap_toggle": {"enabled": asap_toggle.enabled, "checked": asap_toggle.checked}
                                        }
                                        internal.lock_ui()
                                        backend.run_project(window_setting, "Aptos", tab_name)
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
                                    save_config_dialog.project_name = "Aptos"
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
