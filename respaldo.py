# Importamos el módulo necesario
from qgis.core import QgsVectorFileWriter

# Definimos la carpeta donde queremos guardar los shapefiles
output_folder = 'D:/Ervin Duran Aguilar/Backup/Chapi_Mayu_14082023/'

# Obtenemos una lista de las capas activas del proyecto
active_layers = [layer for layer in QgsProject.instance().mapLayers().values() if layer.isValid() and layer.type() == QgsMapLayer.VectorLayer]

# Recorremos la lista de capas activas
for layer in active_layers:
    # Obtenemos el nombre de la capa
    layer_name = layer.name()
    # Creamos el nombre del archivo de salida, usando el nombre de la capa y la extensión .shp
    output_file = output_folder + layer_name + '.shp'
    # Guardamos la capa como shapefile en la carpeta de salida
    QgsVectorFileWriter.writeAsVectorFormat(layer, output_file, 'utf-8', layer.crs(), 'ESRI Shapefile')












# Ervin Duran