import QtQuick
import Felgo
import "../components"

import "../js/Validator.js" as Validator

AppPage {
  function displayErrorText(errorMessage) {
    showErrorItem.text = errorMessage
  }

  function clearErrorText() {
    showErrorItem.text = ""
  }

  id: page
  navigationBarHidden: false
  signal verifyCodeCorrect(string email, string code)

  Connections {
    target: g_apiManager
    onForgotPasswordCorrect: function () {
      console.log("Forgot Password correct ")
      activityIndicatorBarItem.visible = false
      emailAddressField.readOnly = !emailAddressField.readOnly
      emailAddressField.showClearButton = !emailAddressField.showClearButton
      emailAddressField.clickEnabled = !emailAddressField.clickEnabled
      emailAddressField.textColor = "grey"
      page.state = "showVerifyCode"
      clearErrorText()
    }
    onForgotPasswordFailed: function (errorMessage) {
      console.log("Forgot Password failed: ", errorMessage)
      activityIndicatorBarItem.visible = false
      displayErrorText(errorMessage)
    }
    onForgotPasswordCheckTokenCorrect: function () {
      console.log("Forgot Password Check Token correct ")
      page.verifyCodeCorrect(emailAddressField.text, verifyCodeField.text)
      activityIndicatorBarItem.visible = false
      clearErrorText()
    }
    onForgotPasswordCheckTokenFailed: function (errorMessage) {
      console.log("Forgot Password Check Token failed: ", errorMessage)
      activityIndicatorBarItem.visible = false
      displayErrorText(errorMessage)
    }
  }

  function toggleSendEmailButton(email) {
    functionalButton.enabled = Validator.validateEmail(email)
  }

  rightBarItem: ActivityIndicatorBarItem {
    id: activityIndicatorBarItem
    visible: false
  }

  Column {
    id: topColumnLayout
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
      text: "Enter the e-mail address"
      fontSize: sp(24)
      font.bold: true
    }
    AppText {
      anchors.horizontalCenter: parent.horizontalCenter
      text: "provided when creating your account"
      fontSize: sp(16)
      bottomPadding: dp(60)
    }
  }

  ErrorDisplay {
    id: showErrorItem
    anchors.bottom: emailAddressField.top
  }

  CustomTextField {
    id: emailAddressField
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: topColumnLayout.bottom
    inputMode: 2
    placeholderText: "Email address"
    onTextChanged: {
      toggleSendEmailButton(emailAddressField.text)
      clearErrorText()
    }
  }

  Rectangle {
    id: dummyRec1
    width: parent
    height: dp(5)
    anchors.top: emailAddressField.bottom
    opacity: 0
  }

  CustomTextField {
    id: verifyCodeField
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: dummyRec1.bottom
    inputMode: 2
    placeholderText: "Verify code"
    onTextChanged: {
      clearErrorText()
    }
  }

  AppButton {
    id: functionalButton
    anchors.horizontalCenter: parent.horizontalCenter
    flat: false
    backgroundColor: GlobalProperties.leadingColor
    borderColor: GlobalProperties.leadingColor
    textColorPressed: GlobalProperties.leadingColor
    borderColorPressed: GlobalProperties.leadingColor
    textColor: "white"
    enabled: false
    width: dp(320)
    height: dp(50)
    radius: dp(15)
    onClicked: {
      activityIndicatorBarItem.visible = true
      if (page.state === "hideVerifyCode") {
        console.log("Functional Button clicked - SEND EMAIL")
        g_apiManager.forgotPassword(emailAddressField.text)
      } else if (page.state === "showVerifyCode") {
        console.log("Functional Button clicked - VERIFY CODE")
        g_apiManager.forgotPasswordCheckToken(emailAddressField.text,
                                              verifyCodeField.text)
      } else {
        console.log("Functional Button clicked - elseStatement")
      }
    }
  }

  state: "hideVerifyCode"
  states: [
    State {
      name: "showVerifyCode"
      AnchorChanges {
        target: functionalButton
        anchors.top: verifyCodeField.bottom
      }
      PropertyChanges {
        target: verifyCodeField
        opacity: 1
      }
      PropertyChanges {
        target: functionalButton
        text: "Verify"
      }
    },
    State {
      name: "hideVerifyCode"
      AnchorChanges {
        target: functionalButton
        anchors.top: emailAddressField.bottom
      }
      PropertyChanges {
        target: verifyCodeField
        opacity: 0
      }
      PropertyChanges {
        target: functionalButton
        text: "Send Email"
      }
    }
  ]

  transitions: Transition {
    AnchorAnimation {
      duration: 1000
      easing.type: Easing.OutBounce
    }
    NumberAnimation {
      properties: "opacity"
      duration: 500
    }
  }
}
