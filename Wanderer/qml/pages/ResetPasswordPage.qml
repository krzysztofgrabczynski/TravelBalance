import QtQuick
import Felgo
import "../components"

import "../js/Validator.js" as Validator

AppPage {

  function changeMatchRequirementsColor(password, confirmationPassword) {
    if (Validator.passwordsMatch(password, confirmationPassword)) {
      passwordRequirement5.itemsColor = "green"
    } else {
      passwordRequirement5.itemsColor = "red"
    }
  }

  function changeRequirementsColor(password, confirmationPassword) {
    if (password.length >= 8) {
      passwordRequirement1.itemsColor = "green"
    } else {
      passwordRequirement1.itemsColor = "red"
    }

    if (Validator.containsSpecialCharacter(password)) {
      passwordRequirement2.itemsColor = "green"
    } else {
      passwordRequirement2.itemsColor = "red"
    }

    if (Validator.containsUpperLetter(password)) {
      passwordRequirement3.itemsColor = "green"
    } else {
      passwordRequirement3.itemsColor = "red"
    }

    if (Validator.containsNumber(password)) {
      passwordRequirement4.itemsColor = "green"
    } else {
      passwordRequirement4.itemsColor = "red"
    }

    if (Validator.passwordsMatch(password, confirmationPassword)) {
      passwordRequirement5.itemsColor = "green"
    } else {
      passwordRequirement5.itemsColor = "red"
    }
  }

  function toggleResetPasswordButton(password, passwordRepeated) {
    resetPasswordButton.enabled = Validator.validatePassword(password,
                                                             passwordRepeated)
  }

  signal passwordSuccesfullyChanged

  Connections {
    target: g_apiManager
    onForgotPasswordConfirmCorrect: function () {
      console.log("Forgot Password Confirm correct ")
      console.log("Maybe display dialog window (???????) ")
      activityIndicatorBarItem.visible = false
      passwordSuccesfullyChanged()
    }
    onForgotPasswordConfirmFailed: function (errorMessage) {
      console.log("Forgot Password Confirm failed: ", errorMessage)
      activityIndicatorBarItem.visible = false
    }
  }

  id: page
  navigationBarHidden: false

  property string email
  property string verifyCode

  signal correctRegistrationRequestSent

  rightBarItem: ActivityIndicatorBarItem {
    id: activityIndicatorBarItem
    visible: false
  }

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
      text: qsTr("Insert new password!")
      fontSize: sp(24)
      font.bold: true
      bottomPadding: 30
    }
    bottomPadding: dp(10)
  }

  CustomTextField {
    id: passwordTextField
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: columnLayout.bottom
    inputMode: 4
    placeholderText: "New password"
    onTextChanged: {
      changeRequirementsColor(passwordTextField.text,
                              confirmPasswordTextField.text)
      toggleResetPasswordButton(passwordTextField.text,
                                confirmPasswordTextField.text)
    }
    onFocusToggled: {
      page.state = page.state
          === "downConfirmPassword" ? "upConfirmPassword" : "downConfirmPassword"
    }
  }

  Rectangle {
    id: dummyRec1
    width: dp(300)
    height: dp(10)
    visible: false
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: passwordTextField.bottom
  }

  PasswordRequirement {
    id: passwordRequirement1
    anchors.left: passwordTextField.left
    anchors.top: dummyRec1.bottom
    text: qsTr("Password should be at least 8 characters long.")
  }

  PasswordRequirement {
    id: passwordRequirement2
    anchors.left: passwordTextField.left
    anchors.top: passwordRequirement1.bottom
    text: qsTr("Password should contain at least one special character.")
  }

  PasswordRequirement {
    id: passwordRequirement3
    anchors.left: passwordTextField.left
    anchors.top: passwordRequirement2.bottom
    text: qsTr("Password should contain at least one uppercase letter.")
  }

  PasswordRequirement {
    id: passwordRequirement4
    anchors.left: passwordTextField.left
    anchors.top: passwordRequirement3.bottom
    text: qsTr("Password should contain at least one number.")
  }

  Rectangle {
    id: dummyRec2
    width: parent
    visible: false
    height: dp(10)
    anchors.top: passwordRequirement4.bottom
  }

  CustomTextField {
    id: confirmPasswordTextField
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: dummyRec1.bottom
    inputMode: 4
    placeholderText: qsTr("Confirm new password")
    onTextChanged: {
      changeMatchRequirementsColor(passwordTextField.text,
                                   confirmPasswordTextField.text)
      toggleResetPasswordButton(passwordTextField.text,
                                confirmPasswordTextField.text)
    }
    onFocusToggled: {
      page.state = page.state === "downPasswordButton" ? "upPasswordButton" : "downPasswordButton"
    }
  }

  Rectangle {
    id: dummyRec3
    width: parent
    height: dp(10)
    anchors.top: confirmPasswordTextField.bottom
  }

  PasswordRequirement {
    id: passwordRequirement5
    anchors.left: passwordTextField.left
    anchors.top: dummyRec3.bottom
    text: qsTr("Password should match each other.")
  }

  Rectangle {
    id: dummyRec4
    width: parent
    height: dp(10)
    anchors.top: passwordRequirement5.bottom
  }

  AppButton {
    id: resetPasswordButton
    flat: false
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: dummyRec3.bottom
    backgroundColor: GlobalProperties.leadingColor
    borderColor: GlobalProperties.leadingColor
    textColor: "white"
    textColorPressed: GlobalProperties.leadingColor
    borderColorPressed: GlobalProperties.leadingColor
    text: qsTr("Reset Password")
    enabled: false
    width: dp(320)
    height: dp(50)
    radius: dp(15)
    onClicked: {
      console.log("Reset password button clicked")
      activityIndicatorBarItem.visible = true
      g_apiManager.forgotPasswordConfirm(page.email, page.verifyCode,
                                         passwordTextField.text,
                                         confirmPasswordTextField.text)
    }
  }

  state: "upConfirmPassword"
  states: [
    State {
      name: "upConfirmPassword"

      AnchorChanges {
        target: confirmPasswordTextField
        anchors.top: dummyRec1.bottom
      }
      PropertyChanges {
        target: passwordRequirement1
        opacity: 0
      }
      PropertyChanges {
        target: passwordRequirement2
        opacity: 0
      }
      PropertyChanges {
        target: passwordRequirement3
        opacity: 0
      }
      PropertyChanges {
        target: passwordRequirement4
        opacity: 0
      }
    },
    State {
      name: "downConfirmPassword"
      AnchorChanges {
        target: confirmPasswordTextField
        anchors.top: dummyRec2.bottom
      }
      PropertyChanges {
        target: passwordRequirement1
        opacity: 1
      }
      PropertyChanges {
        target: passwordRequirement2
        opacity: 1
      }
      PropertyChanges {
        target: passwordRequirement3
        opacity: 1
      }
      PropertyChanges {
        target: passwordRequirement4
        opacity: 1
      }
    },
    State {
      name: "upPasswordButton"

      AnchorChanges {
        target: resetPasswordButton
        anchors.top: dummyRec3.bottom
      }
      PropertyChanges {
        target: passwordRequirement5
        opacity: 0
      }
    },
    State {
      name: "downPasswordButton"
      AnchorChanges {
        target: resetPasswordButton
        anchors.top: dummyRec4.bottom
      }
      PropertyChanges {
        target: passwordRequirement5
        opacity: 1
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
