import QtQuick
import Felgo
import "."

//property int inputModeDefault: 0
//property int inputModeUsername: 1
//property int inputModeEmail: 2
//property int inputModeUrl: 3
//property int inputModePassword: 4
AppPaper {
  id: root
  property string placeholderText
  property alias inputMode: textField.inputMode
  property alias text: textField.text
  property alias readOnly: textField.readOnly
  property alias textColor: textField.textColor
  property alias showClearButton: textField.showClearButton
  property alias clickEnabled: textField.clickEnabled
  property alias borderColor: textField.borderColor
  signal focusToggled

  shadowSizeDefault: dp(5)
  width: dp(300)
  height: dp(40)
  radius: dp(15)
  AppTextField {
    id: textField
    anchors.fill: parent
    placeholderText: root.placeholderText
    passwordVisibleButton.color: GlobalProperties.leadingColor
    radius: dp(20)
    onFocusChanged: {
      focusToggled()
    }
  }
}
