import QtQuick
import Felgo
import "../components"

AppPage {
  GlobalVariables {
    id: globalVariables
  }
  navigationBarHidden: true

  Column {
    id: columnLayout
    anchors.horizontalCenter: parent.horizontalCenter
    spacing: dp(5)

    GlobalIcon {
      id: icon
      anchors.horizontalCenter: parent.horizontalCenter
      width: dp(100)
      height: dp(200)
    }

    AppText {
      anchors.horizontalCenter: parent.horizontalCenter
      text: "Join the adventure!"
      fontSize: sp(24)
      font.bold: true
      bottomPadding: 30
    }

    CustomTextField {
      id: usernameTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 0
      placeholderText: "Username"
    }

    CustomTextField {
      id: passwordTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 4
      placeholderText: "Password"
      onTextChanged: {
        console.log("Password: " + passwordTextField.text)
      }
    }

    CustomTextField {
      id: confirmPasswordTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 4
      placeholderText: "Confirm Password"
      onTextChanged: {
        console.log("Confirm Password: " + passwordTextField.text)
      }
    }

    CustomTextField {
      id: emailAddressTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 2
      placeholderText: "Email address"
    }
  }

  AppButton {
    id: join
    flat: false
    anchors.horizontalCenter: parent.horizontalCenter
    y: parent.height - nativeUtils.safeAreaInsets.bottom - join.height
    backgroundColor: globalVariables.leadingColor
    borderColor: globalVariables.leadingColor
    textColor: "white"
    textColorPressed: globalVariables.leadingColor
    borderColorPressed: globalVariables.leadingColor
    text: "Join"
    width: dp(320)
    height: dp(50)
    radius: dp(15)
    onClicked: {
      if (passwordTextField.text === confirmPasswordTextField.text) {
        g_apiManager.registerUser(usernameTextField.text,
                                  passwordTextField.text)
      } else {
        nativeUtils.displayMessageBox("Warning", "Passwords do not match!", 1)
      }
    }
  }
}
