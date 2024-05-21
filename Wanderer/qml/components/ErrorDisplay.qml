import QtQuick
import Felgo

Rectangle {
  property alias text: showErrorText.text

  anchors.horizontalCenter: parent.horizontalCenter
  height: showErrorText.height
  AppText {
    id: showErrorText
    anchors.horizontalCenter: parent.horizontalCenter
    fontSize: sp(10)
    color: "red"
  }
}
