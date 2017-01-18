//var entity;
//var entity_list;
//
//function createComponentObjects () {
//    entity_list_component = Qt.createComponent("EntityList.qml");
//    entity_component      = Qt.createComponent("Entity.qml");
//    if (entity_component.status == Component.Ready && entity_list_component.status == Component.Ready)
//        finishCreation();
//    else
//        entity_list_component.statusChanged.connect(finishCreation);
//}
//
//function finishCreation() {
//    if (component.status == Component.Ready) {
//        for (var row = 0; row < 8; ++row) {
//            for (var col = 0; col < 8; ++col) {
//                entity = component.createObject(root, {"position" : Qt.vector3d(0, 0, 0),
//                                                       "rotation" : Qt.vector3d(0, 0, 0),
//                                                       "scale"    : Qt.vector3d(9.0, 9.0, 9.0),
//                                                       "color"    : Qt.vector3d(0.5, 0.5, 0.5)});
//            }
//        }
//
//        if (entity == null) {
//            console.log("Error creating object");
//        } else if (component.status == Component.Error) {
//            // Error Handling
//            console.log("Error loading component:", component.errorString());
//        }
//    }
//}