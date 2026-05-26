from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsProject,
    QgsField,
    QgsFeature,
    QgsVectorLayer,
    QgsSpatialIndex
)

# =========================
# NOMBRES DE LAS CAPAS
# =========================
nombre_capa_puntos = 'd_predios_agregado_01'
nombre_capa_poligonos = 'lim_mpio_5050_05_2024'

# =========================
# CARGAR CAPAS
# =========================
capa_puntos = QgsProject.instance().mapLayersByName(nombre_capa_puntos)[0]
capa_poligonos = QgsProject.instance().mapLayersByName(nombre_capa_poligonos)[0]

# =========================
# CREAR NUEVA CAPA
# =========================
crs = capa_poligonos.crs().authid()

nueva_capa = QgsVectorLayer(
    f'Polygon?crs={crs}',
    'municipios_con_conteo',
    'memory'
)

provider = nueva_capa.dataProvider()

# Copiar campos originales
provider.addAttributes(capa_poligonos.fields())

# Agregar nuevo campo de conteo
provider.addAttributes([
    QgsField('conteo_pts', QVariant.Int)
])

nueva_capa.updateFields()

# =========================
# ÍNDICE ESPACIAL
# =========================
index = QgsSpatialIndex(capa_puntos.getFeatures())

# =========================
# PROCESAR POLÍGONOS
# =========================
features_nuevas = []

for pol in capa_poligonos.getFeatures():

    geom_pol = pol.geometry()

    # Buscar candidatos usando bounding box
    candidatos_ids = index.intersects(geom_pol.boundingBox())

    conteo = 0

    for pid in candidatos_ids:
        punto = capa_puntos.getFeature(pid)

        if geom_pol.contains(punto.geometry()):
            conteo += 1

    # Crear nuevo feature
    nuevo_feat = QgsFeature()

    nuevo_feat.setGeometry(geom_pol)

    attrs = pol.attributes()
    attrs.append(conteo)

    nuevo_feat.setAttributes(attrs)

    features_nuevas.append(nuevo_feat)

# =========================
# AGREGAR FEATURES
# =========================
provider.addFeatures(features_nuevas)

# =========================
# AGREGAR AL PROYECTO
# =========================
QgsProject.instance().addMapLayer(nueva_capa)

print("Proceso completado.")