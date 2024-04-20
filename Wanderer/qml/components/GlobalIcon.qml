import Felgo
import QtQuick 2.0
import "."

// FOR RELEASE UNCOMMENTTHIS


/*
AppImage {
  width: InsertWidth as below
  height: InsertHeight as below
  defaultSource: "qrc:/assets/tent.ico"
}
*/
Rectangle {
  AppIcon {
    id: icon
    size: dp(30)
    color: GlobalProperties.leadingColor
    iconType: IconType.heart
    anchors.centerIn: parent
  }
}
