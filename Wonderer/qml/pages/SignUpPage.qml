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
            && passwordTextField.text.lenth !== 0) {
          redToGreen5.start()
        } else {
          greenToRed5.start()
        }
      }
    }

    CustomTextField {
      id: confirmPasswordTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 4
      placeholderText: "Confirm Password"
      onTextChanged: {
        if (passwordTextField.text === confirmPasswordTextField.text
            && passwordTextField.text.lenth !== 0) {
          redToGreen5.start()
        } else {
          greenToRed5.start()
        }
      }
    }

    CustomTextField {
      id: emailAddressTextField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 2
      placeholderText: "Email address"
    }
    bottomPadding: dp(10)
  }

  Rectangle {
    id: dummyRec
    width: dp(300)
    height: dp(0)
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: columnLayout.bottom
  }

  PasswordRequirement {
    id: passwordRequirement1
    anchors.left: dummyRec.left
    anchors.top: dummyRec.bottom
    text: "Password should be at least 8 characters long."
  }

  PasswordRequirement {
    id: passwordRequirement2
    anchors.left: dummyRec.left
    anchors.top: passwordRequirement1.bottom
    text: "Password should contain at least one special character."
  }

  PasswordRequirement {
    id: passwordRequirement3
    anchors.left: dummyRec.left
    anchors.top: passwordRequirement2.bottom
    text: "Password should contain at least one uppercase letter."
  }

  PasswordRequirement {
    id: passwordRequirement4
    anchors.left: dummyRec.left
    anchors.top: passwordRequirement3.bottom
    text: "Password should contain at least one number."
  }

  PasswordRequirement {
    id: passwordRequirement5
    anchors.left: dummyRec.left
    anchors.top: passwordRequirement4.bottom
    text: "Password should match each other."
  }

  PropertyAnimation {
    id: redToGreen1
    target: passwordRequirement1
    property: "itemsColor"
    from: itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed1
    target: passwordRequirement1
    property: "itemsColor"
    from: itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
  }

  PropertyAnimation {
    id: redToGreen2
    target: passwordRequirement2
    property: "itemsColor"
    from: itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed2
    target: passwordRequirement2
    property: "itemsColor"
    from: itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
  }

  PropertyAnimation {
    id: redToGreen3
    target: passwordRequirement3
    property: "itemsColor"
    from: itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed3
    target: passwordRequirement3
    property: "itemsColor"
    from: itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
  }

  PropertyAnimation {
    id: redToGreen4
    target: passwordRequirement4
    property: "itemsColor"
    from: itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed4
    target: passwordRequirement4
    property: "itemsColor"
    from: itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
  }

  PropertyAnimation {
    id: redToGreen5
    target: passwordRequirement5
    property: "itemsColor"
    from: itemsColor === "red" ? "red" : "green"
    to: "green"
    duration: 200
  }

  PropertyAnimation {
    id: greenToRed5
    target: passwordRequirement5
    property: "itemsColor"
    from: itemsColor === "green" ? "green" : "red"
    to: "red"
    duration: 200
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
