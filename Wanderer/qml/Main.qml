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
        onSwitchToMainPage: navigationStackView.clearAndPush(mainPage)
      }
    }

    Component {
      id: signUpPage
      SignUpPage {
        onCorrectRegistrationRequestSent: navigationStackView.popAllExceptFirst(
                                            )
      }
    }

    Component {
      id: forgotPasswordEmailPage
      ForgotPasswordEmailPage {
        onVerifyCodeCorrect: function (email, code) {
          var resetPage = resetPasswordPage.createObject(navigationStackView, {
                                                           "email": email,
                                                           "verifyCode": code
                                                         })
          navigationStackView.push(resetPage)
        }
      }
    }

    Component {
      id: resetPasswordPage
      ResetPasswordPage {
        onPasswordSuccesfullyChanged: navigationStackView.clearAndPush(
                                        loginPage)
      }
    }

    Component {
      id: mainPage
      MainPage {
        onLogout: navigationStackView.clearAndPush(loginPage)
      }
    }
  }
}
