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
    }

    CustomTextField {
      id: confirmPasswordTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 4
      placeholderText: "Confirm Password"
    }

    CustomTextField {
      id: emailAddressTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 2
      placeholderText: "Email address"
    }

    AppButton {
      id: join
      flat: false
      backgroundColor: "#286e34"
      borderColor: "#286e34"
      textColor: "white"
      textColorPressed: "#286e34"
      borderColorPressed: "#286e34"
      text: "Join"
      width: dp(320)
      height: dp(50)
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
}
