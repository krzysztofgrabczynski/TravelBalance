import QtQuick
import Felgo
import "../components"

AppPage {
  function containsSpecialCharacter(text) {
    var specialCharacters = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/
    return specialCharacters.test(text)
  }
  function containsNumber(text) {
    var numberPattern = /[0-9]+/
    return numberPattern.test(text)
  }
  function containsUpperLetter(text) {
    var upperLetter = /[A-Z]/
    return upperLetter.test(text)
  }
  function validatePassword(password) {
    var isValid = true

    if (password.length < 8) {
      isValid = false
    }

    if (!containsSpecialCharacter(password)) {
      isValid = false
    }

    if (!containsUpperLetter(password)) {
      isValid = false
    }

    if (!containsNumber(password)) {
      isValid = false
    }

    if (password !== confirmPasswordTextField.text || password.length === 0) {
      isValid = false
    }

    return isValid
  }
  function changeMatchRequirementsColor(password, confirmationPassword) {
    if (password === confirmationPassword && password.length > 0) {
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

    if (containsSpecialCharacter(password)) {
      passwordRequirement2.itemsColor = "green"
    } else {
      passwordRequirement2.itemsColor = "red"
    }

    if (containsUpperLetter(password)) {
      passwordRequirement3.itemsColor = "green"
    } else {
      passwordRequirement3.itemsColor = "red"
    }

    if (containsNumber(password)) {
      passwordRequirement4.itemsColor = "green"
    } else {
      passwordRequirement4.itemsColor = "red"
    }

    if (password === confirmationPassword && password.length > 0) {
      passwordRequirement5.itemsColor = "green"
    } else {
      passwordRequirement5.itemsColor = "red"
    }
  }
  function toggleJoinButton() {
    joinButton.enabled = validatePassword(passwordTextField.text)
        && emailAddressTextField.text.length !== 0
        && usernameTextField.text.length !== 0
  }

  id: page
  navigationBarHidden: false

  signal correctRegistrationRequestSent

  Connections {
    target: g_apiManager
    onRegisterCorrect: {
      console.log("Register Correct")
      nativeUtils.displayMessageBox(
            qsTr("E-mail sent!"), qsTr(
              "Please check your email and confirm your account by clicking the provided link."))
    }
    onRegisterFailed: {
      console.log("Register Failed")
    }
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
      text: qsTr("Join the adventure!")
      fontSize: sp(24)
      font.bold: true
      bottomPadding: 30
    }
    bottomPadding: dp(10)
  }

  CustomTextField {
    id: usernameTextField
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: columnLayout.bottom
    inputMode: 0
    placeholderText: qsTr("Username")
    onTextChanged: {
      toggleJoinButton()
    }
  }

  Rectangle {
    id: dummyRec1
    width: parent
    height: dp(10)
    anchors.top: usernameTextField.bottom
  }

  CustomTextField {
    id: passwordTextField
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: dummyRec1.bottom
    inputMode: 4
    placeholderText: "Password"
    onTextChanged: {
      changeRequirementsColor(passwordTextField.text,
                              confirmPasswordTextField.text)

      validatePassword(passwordTextField.text, confirmPasswordTextField.text)
      toggleJoinButton()
    }
    onFocusToggled: {
      page.state = page.state
          === "downConfirmPassword" ? "upConfirmPassword" : "downConfirmPassword"
    }
  }

  Rectangle {
    id: dummyRec2
    width: dp(300)
    height: dp(10)
    visible: false
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: passwordTextField.bottom
  }

  PasswordRequirement {
    id: passwordRequirement1
    anchors.left: usernameTextField.left
    anchors.top: dummyRec2.bottom
    text: qsTr("Password should be at least 8 characters long.")
  }

  PasswordRequirement {
    id: passwordRequirement2
    anchors.left: usernameTextField.left
    anchors.top: passwordRequirement1.bottom
    text: qsTr("Password should contain at least one special character.")
  }

  PasswordRequirement {
    id: passwordRequirement3
    anchors.left: usernameTextField.left
    anchors.top: passwordRequirement2.bottom
    text: qsTr("Password should contain at least one uppercase letter.")
  }

  PasswordRequirement {
    id: passwordRequirement4
    anchors.left: usernameTextField.left
    anchors.top: passwordRequirement3.bottom
    text: qsTr("Password should contain at least one number.")
  }

  Rectangle {
    id: dummyRec3
    width: parent
    visible: false
    height: dp(10)
    anchors.top: passwordRequirement4.bottom
  }

  CustomTextField {
    id: confirmPasswordTextField
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: dummyRec2.bottom
    inputMode: 4
    placeholderText: qsTr("Confirm Password")
    onTextChanged: {
      changeMatchRequirementsColor(passwordTextField.text,
                                   confirmPasswordTextField.text)

      validatePassword(passwordTextField.text, confirmPasswordTextField.text)
      toggleJoinButton()
    }
    onFocusToggled: {
      page.state = page.state === "downEmailAddress" ? "upEmailAddress" : "downEmailAddress"
    }
  }

  Rectangle {
    id: dummyRec4
    width: parent
    height: dp(10)
    anchors.top: confirmPasswordTextField.bottom
  }

  PasswordRequirement {
    id: passwordRequirement5
    anchors.left: usernameTextField.left
    anchors.top: dummyRec4.bottom
    text: qsTr("Password should match each other.")
  }

  Rectangle {
    id: dummyRec5
    width: parent
    height: dp(10)
    anchors.top: passwordRequirement5.bottom
  }

  CustomTextField {
    id: emailAddressTextField
    anchors.top: dummyRec4.bottom
    anchors.horizontalCenter: parent.horizontalCenter
    inputMode: 2
    placeholderText: qsTr("Email address")
    onTextChanged: {
      toggleJoinButton()
    }
  }

  states: [
    State {
      name: "upConfirmPassword"

      AnchorChanges {
        target: confirmPasswordTextField
        anchors.top: dummyRec2.bottom
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
        anchors.top: dummyRec3.bottom
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
      name: "upEmailAddress"

      AnchorChanges {
        target: emailAddressTextField
        anchors.top: dummyRec4.bottom
      }
      PropertyChanges {
        target: passwordRequirement5
        opacity: 0
      }
    },
    State {
      name: "downEmailAddress"
      AnchorChanges {
        target: emailAddressTextField
        anchors.top: dummyRec5.bottom
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

  AppButton {
    id: joinButton
    flat: false
    anchors.horizontalCenter: parent.horizontalCenter
    y: parent.height - nativeUtils.safeAreaInsets.bottom - joinButton.height
    backgroundColor: GlobalProperties.leadingColor
    borderColor: GlobalProperties.leadingColor
    textColor: "white"
    textColorPressed: GlobalProperties.leadingColor
    borderColorPressed: GlobalProperties.leadingColor
    text: qsTr("Join")
    enabled: false
    width: dp(320)
    height: dp(50)
    radius: dp(15)
    onClicked: {
      g_apiManager.registerUser(usernameTextField.text, passwordTextField.text,
                                confirmPasswordTextField.text,
                                emailAddressTextField.text)
    }
  }

  Connections {
    target: NativeUtils
    onMessageBoxFinished: function (accepted) {
      if (accepted) {
        correctRegistrationRequestSent()
      }
    }
  }
}
