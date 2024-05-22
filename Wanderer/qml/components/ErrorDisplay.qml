import QtQuick
import Felgo

Rectangle {
  property alias text: showErrorText.text

  anchors.horizontalCenter: parent.horizontalCenter
  height: showErrorText.height + dp(10)
  AppText {
    id: showErrorText
    anchors.horizontalCenter: parent.horizontalCenter
    fontSize: sp(10)
    color: "red"
  }
}
