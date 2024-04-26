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
        onForgotPasswordClicked: navigationStackView.push(
                                   forgotPasswordEmailPage)
      }
    }

    Component {
      id: signUpPage
      SignUpPage {
        onRegisterButtonClicked: navigationStackView.popAllExceptFirst()
      }
    }

    Component {
      id: forgotPasswordEmailPage
      ForgotPasswordEmailPage {}
    }
  }
}
