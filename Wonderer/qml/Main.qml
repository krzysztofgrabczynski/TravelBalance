import Felgo
import QtQuick
import "./components"
import "./pages"

App {
  NavigationStack {
    id: navigationStackView
    initialPage: loginPage

    Component {
      id: loginPage
      LoginPage {
        onSignUpClicked: navigationStackView.push(signUpPage)
      }
    }

    Component {
      id: signUpPage
      SignUpPage {}
    }
  }
}
