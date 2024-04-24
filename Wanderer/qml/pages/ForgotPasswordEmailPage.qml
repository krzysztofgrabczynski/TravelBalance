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
      bottomPadding: 60
    }
  }

  Column {
    id: bottomColumnLayout
    anchors.horizontalCenter: parent.horizontalCenter
    spacing: dp(5)
    anchors.top: topColumnLayout.bottom

    CustomTextField {
      id: emailAddressField
      anchors.horizontalCenter: parent.horizontalCenter
      inputMode: 2
      placeholderText: "Email address"
    }
    AppButton {
      anchors.horizontalCenter: parent.horizontalCenter
      id: sendEmailButton
      flat: false
      backgroundColor: GlobalProperties.leadingColor
      borderColor: GlobalProperties.leadingColor
      textColorPressed: GlobalProperties.leadingColor
      borderColorPressed: GlobalProperties.leadingColor
      textColor: "white"
      text: "Send Email"
      width: dp(320)
      height: dp(50)
      radius: dp(15)
      onClicked: {
        console.log("Email sent - TBD")
        emailAddressField.readOnly = !emailAddressField.readOnly
        emailAddressField.showClearButton = !emailAddressField.showClearButton
        emailAddressField.clickEnabled = !emailAddressField.clickEnabled
        if (emailAddressField.readOnly)
          emailAddressField.textColor = "grey"
        else
          emailAddressField.textColor = "black"
      }
    }
  }

  states: [
    State {
      name: "showVerifyCode"
      AnchorChanges {
        //target: confirmPasswordTextField
        //anchors.top: dummyRec2.bottom
      }
    },
    State {
      name: "hideVerifyCode"
      AnchorChanges {
        //target: confirmPasswordTextField
        //anchors.top: dummyRec3.bottom
      }
    }
  ]

  transitions: Transition {
    AnchorAnimation {
      duration: 1000
      easing.type: Easing.OutBounce
    }
  }
}
