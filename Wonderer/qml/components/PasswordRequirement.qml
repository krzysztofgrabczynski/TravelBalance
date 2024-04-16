import QtQuick
import Felgo

Row {
  property alias text: textItem.text
  property color itemsColor: "red"

  spacing: dp(5)
  AppIcon {
    id: iconItem
    anchors.verticalCenter: parent.verticalCenter
    iconType: IconType.close
    color: itemsColor
    size: dp(10)
  }
  AppText {
    id: textItem
    text: "Password should be at least 8 characters long."
    color: itemsColor
    fontSize: dp(10)
  }
}
