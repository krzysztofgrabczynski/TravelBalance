import QtQuick
import QtQuick.Layouts
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
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 0
      placeholderText: "Login"
    }
    CustomTextField {
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 4
      placeholderText: "Password"
    }

    AppButton {
      anchors.horizontalCenter: parent.horizontalCenter
      id: loginButton
      flat: false
      backgroundColor: globalVariables.leadingColor
      borderColor: globalVariables.leadingColor
      textColorPressed: globalVariables.leadingColor
      borderColorPressed: globalVariables.leadingColor
      textColor: "white"
      text: "Login"
      width: dp(320)
      height: dp(50)
    }
  }
  AppButton {
    anchors.top: columnLayout.bottom
    anchors.left: columnLayout.left
    flat: true
    textColor: "black"
    textColorPressed: globalVariables.leadingColor
    text: "Sign up"
    minimumWidth: 0
    minimumHeight: 0
    horizontalMargin: dp(6)
    onClicked: {
      console.log("SignUpClicked")
    }
  }
  AppButton {
    anchors.top: columnLayout.bottom
    anchors.right: columnLayout.right
    flat: true
    textColor: "black"
    textColorPressed: globalVariables.leadingColor
    text: "Forgot password?"
    minimumWidth: 0
    minimumHeight: 0
    horizontalMargin: dp(6)
    onClicked: {
      console.log("LogInClicked")
    }
  }
}
