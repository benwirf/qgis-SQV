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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Ben Wirf'
__date__ = '2019-03-02'
__copyright__ = '(C) 2019 by Ben Wirf'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SpatialQueryWithValues class from file SpatialQueryWithValues.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .spatial_query_with_values import SpatialQueryWithValuesPlugin
    return SpatialQueryWithValuesPlugin()
