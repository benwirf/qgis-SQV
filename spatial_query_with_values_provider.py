# -*- coding: utf-8 -*-

"""
/***************************************************************************
 SpatialQueryWithValues
                                 A QGIS plugin
 Get maximum or minimum vector features for each polygon in an intersecting layer.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-03-02
        copyright            : (C) 2019 by Ben Wirf
        email                : ben.wirf@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Ben Wirf'
__date__ = '2019-03-02'
__copyright__ = '(C) 2019 by Ben Wirf'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingProvider
from .ExtractMaxMinFeaturesInPolygons import ExtractFeaturesInPolygonsWithValues
from .SelectMaxMinFeaturesInPolygons import SelectFeaturesInPolygonsWithValues

iconPath = os.path.dirname(__file__)


class SpatialQueryWithValuesProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

        # Load algorithms
        self.alglist = [ExtractFeaturesInPolygonsWithValues(), SelectFeaturesInPolygonsWithValues()]

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        for alg in self.alglist:
            self.addAlgorithm(alg)

    def icon(self):
        return QIcon(os.path.join(iconPath, "sqv.png"))

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'Spatial Query With Values'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('Spatial Query With Values')

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
