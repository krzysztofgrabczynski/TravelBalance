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
AppIcon {

  size: dp(30)
  color: globalProperties.leadingGreenColor

  iconType: IconType.heart
  GlobalVariables {
    id: globalProperties
  }
}
