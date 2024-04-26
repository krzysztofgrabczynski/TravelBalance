import QtQuick
import QtQuick.Layouts
import Felgo
import "../components"

AppPage {
  function enableLoginButton(loginField, PasswordField) {
    var isValid = true

    if (loginField.length === 0 || PasswordField.length === 0)
      isValid = false

    loginButton.enabled = isValid
  }

  Connections {
    target: g_apiManager
    onLoginCorrect: function (token) {
      console.log("Token:", token)
    }
    onLoginFailed: {
      console.log("Login failed")
    }
  }
  id: page
  navigationBarHidden: false

  signal signUpClicked
  signal forgotPasswordClicked

  Column {
    id: columnLayout
    anchors.horizontalCenter: parent.horizontalCenter
    spacing: dp(5)

    GlobalIcon {
      id: icon
      anchors.horizontalCenter: parent.horizontalCenter
      width: dp(100)
      height: dp(150)
    }

    AppText {
      anchors.horizontalCenter: parent.horizontalCenter
      text: "Welcome back wanderer!"
      fontSize: sp(24)
      font.bold: true
    }
    AppText {
      anchors.horizontalCenter: parent.horizontalCenter
      text: "Create your next journey here."
      fontSize: sp(16)
      bottomPadding: 60
    }

    CustomTextField {
      id: loginTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 0
      placeholderText: "Login"
      onTextChanged: {
        enableLoginButton(loginTextField.text, passwordTextField.text)
      }
    }

    CustomTextField {
      id: passwordTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 4
      placeholderText: "Password"
      onTextChanged: {
        enableLoginButton(loginTextField.text, passwordTextField.text)
      }
    }

    AppButton {
      anchors.horizontalCenter: parent.horizontalCenter
      id: loginButton
      flat: false
      backgroundColor: GlobalProperties.leadingColor
      borderColor: GlobalProperties.leadingColor
      textColorPressed: GlobalProperties.leadingColor
      borderColorPressed: GlobalProperties.leadingColor
      textColor: "white"
      text: qsTr("Login")
      width: dp(320)
      height: dp(50)
      radius: dp(15)
      enabled: false
      onClicked: {
        console.log("Login Clicked")
        g_apiManager.loginUser(loginTextField.text, passwordTextField.text)
      }
    }
  }
  AppButton {
    anchors.top: columnLayout.bottom
    anchors.left: columnLayout.left
    flat: true
    textColor: "black"
    textColorPressed: GlobalProperties.leadingColor
    text: qsTr("Sign up")
    minimumWidth: 0
    minimumHeight: 0
    horizontalMargin: dp(6)
    onClicked: {
      console.log("Sign Up Clicked")
      signUpClicked()
    }
  }
  AppButton {
    anchors.top: columnLayout.bottom
    anchors.right: columnLayout.right
    flat: true
    textColor: "black"
    textColorPressed: GlobalProperties.leadingColor
    text: qsTr("Forgot password?")
    minimumWidth: 0
    minimumHeight: 0
    horizontalMargin: dp(6)
    onClicked: {
      console.log("Forgot Password clicked")
      forgotPasswordClicked()
    }
  }
}
