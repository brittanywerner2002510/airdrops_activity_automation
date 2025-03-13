import QtQuick 2.15
import QtQuick.Controls 2.15

TextField {
    id: path_to_file_field

    property color default_color: "#282c34"
    property color on_focus_color: "#242831"
    property color hovered_color: "#2B2F38"
    property bool read_only: true
    property bool is_valid: true

    QtObject {
        id: internal

        property color dynamic_color: if(path_to_file_field.focus) {
                                        path_to_file_field.hovered ? on_focus_color : default_color
                                   } else {
                                       path_to_file_field.hovered ? hovered_color : default_color
                                   }
    }

    width: 300
    height: 40
    verticalAlignment: Qt.AlignVCenter
    color: "#ffffff"
    readOnly: read_only
    horizontalAlignment: Text.AlignHCenter

    background: Rectangle {
        color: internal.dynamic_color
        border.width: 2
        radius: 10
        border.color: is_valid ? "#00000000" : "#cc0000"
    }

    selectByMouse: true
    selectedTextColor: "#FFFFFF"
    selectionColor: "#ff007f"
    placeholderTextColor: "#81848c"
}
