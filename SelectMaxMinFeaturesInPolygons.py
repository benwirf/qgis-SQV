

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayer, QgsFeatureRequest, QgsProcessing,
                       QgsGeometry, QgsProcessingAlgorithm, QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterFeatureSource, QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterField, QgsSpatialIndex)


class SelectFeaturesInPolygonsWithValues(QgsProcessingAlgorithm):
    INPUT_POLYGONS = 'INPUT_POLYGONS'
    INPUT_ADDITIONAL = 'INPUT_ADDITIONAL'
    VALUE_FIELD = 'VALUE_FIELD'
    M_VAL = 'M_VAL'
    METHOD = 'METHOD'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagRequiresMatchingCrs | QgsProcessingAlgorithm.FlagNoThreading

    def name(self):
        return "Select_max_min_features_in_polygons"

    def tr(self, text):
        return QCoreApplication.translate("Select_max_min_features_in_polygons", text)

    def displayName(self):
        return self.tr("Select max min features in polygons")

    def group(self):
        return self.tr("Vector analysis")

    def groupId(self):
        return "vector_analysis"

    def shortHelpString(self):
        return self.tr("Selects features from a vector layer. Feature selection is based on either \
        maximum or minimum values in an attribute field. The maximum or minimum features are selected for \
        each feature in an intersecting polygon layer.")

    def helpUrl(self):
        return "https://qgis.org"

    def createInstance(self):
        return type(self)()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_POLYGONS,
            self.tr("Input polygon layer"),
            [QgsProcessing.TypeVectorPolygon]))
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT_ADDITIONAL,
            self.tr("Additional input layer"),
            [QgsProcessing.TypeVectorAnyGeometry]))
        self.addParameter(QgsProcessingParameterField(
            self.VALUE_FIELD,
            self.tr("Attribute field"),
            parentLayerParameterName=self.INPUT_ADDITIONAL, type=0, optional=False))
        self.vals = [self.tr("Maximum"), self.tr("Minimum")]
        self.addParameter(QgsProcessingParameterEnum(
            self.M_VAL,
            self.tr("Select Value"),
            options=self.vals, defaultValue=0))
        self.methods = [self.tr('creating new selection'),
            self.tr('adding to current selection'),
            self.tr('removing from current selection'),
            self.tr('selecting within current selection')]
        self.addParameter(QgsProcessingParameterEnum(
            self.METHOD,
            self.tr('Modify current selection by'),
            options=self.methods, defaultValue=0))
        self.addOutput(QgsProcessingOutputVectorLayer(self.OUTPUT, self.tr('Selected (attribute)')))

    def processAlgorithm(self, parameters, context, feedback):
        source_poly = self.parameterAsSource(parameters, self.INPUT_POLYGONS, context)
        source_add = self.parameterAsVectorLayer(parameters, self.INPUT_ADDITIONAL, context)
        val_field = self.parameterAsString(parameters, self.VALUE_FIELD, context)
        feature_value = self.parameterAsEnum(parameters, self.M_VAL, context)
        if feature_value == 0:
            m_val = max
        elif feature_value == 1:
            m_val = min

        max_ids = []
        att_col_idx = source_add.fields().indexFromName(val_field)
        fcount = source_poly.featureCount()
        polygons = source_poly.getFeatures()
        points = source_add.getFeatures()
        index = QgsSpatialIndex()  # this spatial index contains all the features of the point layer
        for point in points:
            index.insertFeature(point)

        for current, polygon in enumerate(polygons):
            if feedback.isCanceled():
                break
            f = int(current + 1)
            pcnt = int(f/fcount * 100/1)
            feedback.setProgress(pcnt)
            ids = []
            vals = []
            poly_geom = polygon.geometry()
            engine = QgsGeometry.createGeometryEngine(poly_geom.constGet())
            engine.prepareGeometry()
            idx_ids = index.intersects(poly_geom.boundingBox())
            for f in source_add.getFeatures(QgsFeatureRequest(idx_ids)):
                geom = f.geometry()
                if engine.contains(geom.constGet()):
                    ids.append(f.id())
                    vals.append(f.attributes()[att_col_idx])
            #Note that the three lines below are all in the polygon feature loop so they are executed once for each polygon feature
            d = dict(zip(ids, vals)) #creates dictionaries with id as key and elevation as value
            if d:
                n_max = m_val(d.values())  #m_val is either max or min depending on combo box selection
                max_ids.append([a for a, b in d.items() if b == n_max])  #gets ids from each dictionary as keys with highest value
        all_max_min_ids = [item for sublist in max_ids for item in sublist]  # creates the flat list from list of lists

        method = self.parameterAsEnum(parameters, self.METHOD, context)
        if method == 0:
            behaviour = QgsVectorLayer.SetSelection
        elif method == 1:
            behaviour = QgsVectorLayer.AddToSelection
        elif method == 2:
            behaviour = QgsVectorLayer.RemoveFromSelection
        elif method == 3:
            behaviour = QgsVectorLayer.IntersectSelection

        source_add.selectByIds(all_max_min_ids, behaviour)

        return {self.OUTPUT: parameters[self.M_VAL]}