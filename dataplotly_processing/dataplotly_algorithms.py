# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DataPlotly
                                 A QGIS plugin
 D3 Plots for QGIS
                              -------------------
        begin                : 2017-03-05
        git sha              : $Format:%H$
        copyright            : (C) 2017 by matteo ghetta
        email                : matteo.ghetta@gmail.com
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

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from DataPlotly.data_plotly_dialog import DataPlotlyDialog

from qgis.utils import plugins

from qgis.core import (QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingUtils,
                       QgsProcessingParameterFileDestination,
                       QgsSettings,
                       QgsProcessingOutputHtml,
                       QgsProcessingOutputVectorLayer,
                       QgsFeatureRequest)

from processing.tools import vector


class DataPlotlyScatterPlot(QgisAlgorithm):

    """This is an example algorithm that takes a vector layer and
    creates a new one just with just those features of the input
    layer that are selected.
    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.
    All Processing algorithms should extend the GeoAlgorithm class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    XFIELD = 'XFIELD'
    YFIELD = 'YFIELD'

    def __init__(self):
        super().__init__()
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

    def initAlgorithm(self, config=None):

        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
                                                              self.tr('Input layer')))

        self.addParameter(QgsProcessingParameterField(self.XFIELD,
                                                      self.tr('X attribute'),
                                                      parentLayerParameterName=self.INPUT,
                                                      type=QgsProcessingParameterField.Any))

        self.addParameter(QgsProcessingParameterField(self.YFIELD,
                                                      self.tr('Y attribute'),
                                                      parentLayerParameterName=self.INPUT,
                                                      type=QgsProcessingParameterField.Any))
        # self.addParameter(QgsProcessingParameterFileDestination(self.OUTPUT,
                                                                # self.tr('Scatterplot'),
                                                                # self.tr('HTML files (*.html)')))
        # self.addOutput(QgsProcessingOutputHtml(self.OUTPUT, self.tr('Scatterplot')))
        self.addOutput(QgsProcessingOutputVectorLayer(self.OUTPUT, self.tr('Plot')))


    def name(self):
        # Unique (non-user visible) name of algorithm
        return 'scatter'

    def displayName(self):
        # The name that the user will see in the toolbox
        return self.tr('Scatter Plot')

    def group(self):
        return self.tr('Plots')

    def processAlgorithm(self, parameters, context, feedback):
        """Here is where the processing itself takes place.
        :param parameters:
        :param context:
        """

        layer = self.parameterAsSource(parameters, self.INPUT, context)
        xfieldname = self.parameterAsString(parameters, self.XFIELD, context)
        yfieldname = self.parameterAsString(parameters, self.YFIELD, context)

        fields = layer.fields()

        # get field index for x
        idxX = layer.fields().lookupField(xfieldname)
        # get list of values for x
        x_var = [i[xfieldname] for i in layer.getFeatures(QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry).setSubsetOfAttributes([idxX]))]
        fieldTypeX = fields[idxX].type()

        # get field index for y
        idxY = layer.fields().lookupField(yfieldname)
        # get list of values for y
        y_var = [i[yfieldname] for i in layer.getFeatures(QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry).setSubsetOfAttributes([idxY]))]

        pdic = {}
        pdic['plot_prop'] = {}
        pdic['layout_prop'] = {}

        pdic['plot_type'] = 'scatter'
        pdic['layer'] = layer
        pdic['plot_prop']['x'] = x_var
        pdic['plot_prop']['y'] = y_var

        myplugin = plugins['DataPlotly']
        myplugin.loadPlotNoBlock(pdic)

        # p = DataPlotlyDialog()
        # p.showPlot(pdic)
        # p.show()
        # p.exec_()

        return {self.OUTPUT: None}
