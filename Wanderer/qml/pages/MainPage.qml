import QtQuick
import Felgo
import "../components"

AppPage {
  id: page
  title: "MainPage"

  signal logout

  Connections {
    target: g_apiManager
    onLogoutCorrect: {
      logout()
    }
    onLogoutFailed: function (errorMessage) {
      console.log("Logout failed: ", errorMessage)
    }
  }

  AppButton {
    anchors.centerIn: parent
    width: dp(100)
    height: dp(100)
    backgroundColor: GlobalProperties.leadingColor
    text: "Logout!"
    onClicked: {
      g_apiManager.logoutUser()
    }
  }
}
