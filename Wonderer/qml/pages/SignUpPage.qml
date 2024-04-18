import QtQuick
import Felgo
import "../components"

AppPage {
  function containsSpecialCharacter(text) {
    var specialCharacters = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/
    return specialCharacters.test(text)
  }
  function containsNumber(text) {
    var numberPattern = /[1234567890]/
    return numberPattern.test(text)
  }
  function containsUpperLetter(text) {
    var upperLetter = /[A-Z]/
    return upperLetter.test(text)
  }
  GlobalVariables {
    id: globalVariables
  }
  id: page
  navigationBarHidden: true

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
      text: "Join the adventure!"
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
    placeholderText: "Username"
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
      if (passwordTextField.text.length >= 8) {
        redToGreen1.start()
      } else {
        greenToRed1.start()
      }

      if (containsSpecialCharacter(passwordTextField.text)) {
        redToGreen2.start()
      } else {
        greenToRed2.start()
      }

      if (containsUpperLetter(passwordTextField.text)) {
        redToGreen3.start()
      } else {
        greenToRed3.start()
      }

      if (containsNumber(passwordTextField.text)) {
        redToGreen4.start()
      } else {
        greenToRed4.start()
      }

      if (passwordTextField.text === confirmPasswordTextField.text
          && passwordTextField.text.length > 0) {
        redToGreen5.start()
      } else {
        greenToRed5.start()
      }
    }
    onFocusToggled: {
      console.log("page.state")
      page.state = page.state
          === "downConfirmPassword" ? "upConfirmPassword" : "downConfirmPassword"
      changeOpacity1.start()
      changeOpacity2.start()
      changeOpacity3.start()
      changeOpacity4.start()
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
    text: "Password should be at least 8 characters long."
    opacity: 0
  }

  PasswordRequirement {
    id: passwordRequirement2
    anchors.left: usernameTextField.left
    anchors.top: passwordRequirement1.bottom
    text: "Password should contain at least one special character."
    opacity: 0
  }

  PasswordRequirement {
    id: passwordRequirement3
    anchors.left: usernameTextField.left
    anchors.top: passwordRequirement2.bottom
    text: "Password should contain at least one uppercase letter."
    opacity: 0
  }

  PasswordRequirement {
    id: passwordRequirement4
    anchors.left: usernameTextField.left
    anchors.top: passwordRequirement3.bottom
    text: "Password should contain at least one number."
    opacity: 0
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
    placeholderText: "Confirm Password"
    onTextChanged: {
      if (passwordTextField.text === confirmPasswordTextField.text
          && passwordTextField.text.length > 0) {
        redToGreen5.start()
      } else {
        greenToRed5.start()
      }
    }
    onFocusToggled: {
      console.log("page.statecobf")
      page.state = page.state === "downEmailAddress" ? "upEmailAddress" : "downEmailAddress"
      changeOpacity5.start()
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
    text: "Password should match each other."
    opacity: 0
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
    placeholderText: "Email address"
  }

  PropertyAnimation {
    id: redToGreen1
    target: passwordRequirement1
    property: "itemsColor"
    from: passwordRequirement1.itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed1
    target: passwordRequirement1
    property: "itemsColor"
    from: passwordRequirement1.itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
  }

  PropertyAnimation {
    id: redToGreen2
    target: passwordRequirement2
    property: "itemsColor"
    from: passwordRequirement2.itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed2
    target: passwordRequirement2
    property: "itemsColor"
    from: passwordRequirement2.itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
  }

  PropertyAnimation {
    id: redToGreen3
    target: passwordRequirement3
    property: "itemsColor"
    from: passwordRequirement3.itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed3
    target: passwordRequirement3
    property: "itemsColor"
    from: passwordRequirement3.itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
  }

  PropertyAnimation {
    id: redToGreen4
    target: passwordRequirement4
    property: "itemsColor"
    from: passwordRequirement4.itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed4
    target: passwordRequirement4
    property: "itemsColor"
    from: passwordRequirement4.itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
  }

  PropertyAnimation {
    id: redToGreen5
    target: passwordRequirement5
    property: "itemsColor"
    from: passwordRequirement5.itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed5
    target: passwordRequirement5
    property: "itemsColor"
    from: passwordRequirement5.itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
  }

  PropertyAnimation {
    id: changeOpacity1
    target: passwordRequirement1
    property: "opacity"
    from: passwordRequirement1.opacity // Początkowa wartość przezroczystości
    to: passwordRequirement1.opacity === 1 ? 0 : 1 // Docelowa wartość przezroczystości
    duration: 500
  }

  PropertyAnimation {
    id: changeOpacity2
    target: passwordRequirement2
    property: "opacity"
    from: passwordRequirement2.opacity // Początkowa wartość przezroczystości
    to: passwordRequirement2.opacity === 1 ? 0 : 1 // Docelowa wartość przezroczystości
    duration: 500
  }

  PropertyAnimation {
    id: changeOpacity3
    target: passwordRequirement3
    property: "opacity"
    from: passwordRequirement3.opacity // Początkowa wartość przezroczystości
    to: passwordRequirement3.opacity === 1 ? 0 : 1 // Docelowa wartość przezroczystości
    duration: 500
  }

  PropertyAnimation {
    id: changeOpacity4
    target: passwordRequirement4
    property: "opacity"
    from: passwordRequirement4.opacity // Początkowa wartość przezroczystości
    to: passwordRequirement4.opacity === 1 ? 0 : 1 // Docelowa wartość przezroczystości
    duration: 500
  }

  PropertyAnimation {
    id: changeOpacity5
    target: passwordRequirement5
    property: "opacity"
    from: passwordRequirement5.opacity // Początkowa wartość przezroczystości
    to: passwordRequirement5.opacity === 1 ? 0 : 1 // Docelowa wartość przezroczystości
    duration: 500
  }

  states: [
    State {
      name: "upConfirmPassword"

      AnchorChanges {
        target: confirmPasswordTextField
        anchors.top: dummyRec2.bottom
      }
    },
    State {
      name: "downConfirmPassword"
      AnchorChanges {
        target: confirmPasswordTextField
        anchors.top: dummyRec3.bottom
      }
    },
    State {
      name: "upEmailAddress"

      AnchorChanges {
        target: emailAddressTextField
        anchors.top: dummyRec4.bottom
      }
    },
    State {
      name: "downEmailAddress"
      AnchorChanges {
        target: emailAddressTextField
        anchors.top: dummyRec5.bottom
      }
    }
  ]

  transitions: Transition {
    AnchorAnimation {
      duration: 1000
      easing.type: Easing.OutBounce
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
