import QtQuick
import Felgo

//property int inputModeDefault: 0
//property int inputModeUsername: 1
//property int inputModeEmail: 2
//property int inputModeUrl: 3
//property int inputModePassword: 4
AppPaper {
  GlobalVariables {
    id: globalVariables
  }
  id: root
  property string placeholderText
  property alias inputMode: textField.inputMode
  property alias text: textField.text

  shadowSizeDefault: dp(5)
  width: dp(300)
  height: dp(40)
  radius: dp(15)
  AppTextField {
    id: textField
    anchors.fill: parent
    placeholderText: root.placeholderText
    passwordVisibleButton.color: globalVariables.leadingColor
    radius: dp(20)
  }
}
