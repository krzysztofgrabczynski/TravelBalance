import Felgo
import QtQuick
import "./components"

App {
  GlobalVariables {
    id: globalProperties
  }

  NavigationStack {

    AppPage {
      title: qsTr("Main Page")
    }
  }
}
