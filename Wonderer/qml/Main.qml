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

    Rectangle {
      anchors.centerIn: parent
      width: 100
      height: 100
      color: globalProperties.leadingGreenColor
    }
  }
}
