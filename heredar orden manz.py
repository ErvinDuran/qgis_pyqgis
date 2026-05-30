# Obtener los nombres de las capas
layer1_name = "a_manzanas_05"
layer2_name = "bolivia_predio_seg"

# Obtener las capas por su nombre
layer1 = QgsProject.instance().mapLayersByName(layer1_name)[0]
layer2 = QgsProject.instance().mapLayersByName(layer2_name)[0]

# Crear un diccionario para almacenar los valores heredados
inherited_values = {}

# Obtener los índices de los campos en el layer1
orden_manz_index1 = layer1.fields().indexFromName("orden_manz")


# Obtener los índices de los campos en el layer2
orden_manz_index2 = layer2.fields().indexFromName("orden_manz")


# Recorrer los features del layer1
for feature1 in layer1.getFeatures():
    geom1 = feature1.geometry()
    
    # Filtrar los features en el layer2 que coinciden espacialmente con el feature1
    request = QgsFeatureRequest().setFilterRect(geom1.boundingBox())
    for feature2 in layer2.getFeatures(request):
        geom2 = feature2.geometry()
        
        # Verificar la coincidencia espacial entre los features
        if geom2.intersects(geom1):
            # Obtener los valores de los campos en el feature1
            orden_manz_value1 = feature1[orden_manz_index1]
            
            # Almacenar los valores en el diccionario con el ID del feature2 como clave
            inherited_values[feature2.id()] = {
                "orden_manz": orden_manz_value1,
            }

# Actualizar los campos en el layer2 con los valores heredados
layer2.startEditing()
for feature2 in layer2.getFeatures():
    feature_id = feature2.id()
    
    if feature_id in inherited_values:
        values = inherited_values[feature_id]
        
        # Actualizar los campos en el feature2 con los valores heredados
        feature2[orden_manz_index2] = values["orden_manz"]
        
        # Guardar los cambios en el layer2
        layer2.updateFeature(feature2)

layer2.commitChanges()
layer2.triggerRepaint()