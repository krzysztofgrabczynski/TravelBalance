import QtQuick
import Felgo
import "../components"

AppPage {
  id: page
  navigationBarHidden: false

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

  CustomTextField {
    id: emailAddressField
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: topColumnLayout.bottom
    inputMode: 2
    placeholderText: "Email address"
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
    width: dp(320)
    height: dp(50)
    radius: dp(15)
    onClicked: {
      console.log("Functional Button clicked - TBD")
      emailAddressField.readOnly = !emailAddressField.readOnly
      emailAddressField.showClearButton = !emailAddressField.showClearButton
      emailAddressField.clickEnabled = !emailAddressField.clickEnabled
      if (emailAddressField.readOnly)
        emailAddressField.textColor = "grey"
      else
        emailAddressField.textColor = "black"

      page.state = page.state === "hideVerifyCode" ? "showVerifyCode" : "hideVerifyCode"
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
