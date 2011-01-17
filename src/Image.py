﻿# -*- coding: utf-8 -*-
#
# This file is part of Open Ant.
#
# Open Ant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Open Ant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Open Ant.  If not, see <http://www.gnu.org/licenses/>.

#
# convenience class
#
# By Oipo (kingoipo@gmail.com)

from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.arrays import ArrayDatatype as ADT

import Globals

import numpy

class Image(object):
    '''
    Class for storing image data, position and some opengl stuff
    '''

    def __init__(self, imagepath, textureRect, drawRect, layer, hidden, dynamicity):
        self.imagepath = imagepath
        self.drawRect = drawRect
        self.textureRect = textureRect
        self.layer = layer
        self.dynamicity = dynamicity
        self.textureId = None
        self.offset = None
        self.VBO = None
        self._hidden = hidden

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, hide):
        if self._hidden != hide:
            self._hidden = hide
            Globals.glwidget.hideImage(self, hide)

    def setDrawRect(self, drawRect):
        self.drawRect = drawRect

        if Globals.vbos:
            VBOData = self.createVBOData()
            vertByteCount = ADT.arrayByteCount(VBOData)

            glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBO)
            glBufferSubData(GL_ARRAY_BUFFER_ARB, self.offset*vertByteCount, vertByteCount, VBOData)

    def getVBOData(self):
        x, y, w, h = self.textureRect
        dx, dy, dw, dh = self.drawRect

        VBOData = numpy.zeros((8, 2), 'f')

        VBOData[0, 0] = x #tex
        VBOData[0, 1] = y+h

        VBOData[1, 0] = dx #vert
        VBOData[1, 1] = dy

        VBOData[2, 0] = x+w #tex
        VBOData[2, 1] = y+h

        VBOData[3, 0] = dx+dw #vert
        VBOData[3, 1] = dy

        VBOData[4, 0] = x+w
        VBOData[4, 1] = y

        VBOData[5, 0] = dx+dw
        VBOData[5, 1] = dy+dh

        VBOData[6, 0] = x
        VBOData[6, 1] = y

        VBOData[7, 0] = dx
        VBOData[7, 1] = dy+dh

        return VBOData
