import QtQuick
import Felgo
import "../components"
import "../pages"

AppPage {
  id: page
  signal logout

  Connections {
    target: g_apiManager
    onLogoutCorrect: {
      console.log("Logout correct!")
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
      console.log("Logout clicked!")
      g_apiManager.logoutUser()
    }
  }
  Navigation {
    NavigationItem {
      iconType: IconType.googlewallet
      NavigationStack {}
    }
    NavigationItem {
      iconType: IconType.ambulance
      NavigationStack {}
    }
    NavigationItem {
      iconType: IconType.bomb
      NavigationStack {}
    }
    NavigationItem {
      iconType: IconType.book
      NavigationStack {}
    }
  }
}
