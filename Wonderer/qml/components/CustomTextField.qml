import QtQuick
import Felgo

//property int inputModeDefault: 0
//property int inputModeUsername: 1
//property int inputModeEmail: 2
//property int inputModeUrl: 3
//property int inputModePassword: 4
AppPaper {
  id: root
  property string placeholderText
  property int inputMode

  width: dp(300)
  height: dp(40)

  AppTextField {
    id: textField
    anchors.fill: parent
    placeholderText: root.placeholderText
    inputMode: root.inputMode
  }
}
