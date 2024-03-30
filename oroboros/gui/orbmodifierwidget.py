#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Orbs modifiers widgets.

"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5


__all__ = ['OrbModifierSpinBox']


class OrbModifierSpinBox(PyQt5.QtWidgets.QDoubleSpinBox):
	"""Orb modifier spin box.
	
	For the moment only relative modifiers are supported (percent).
	
	"""
	
	def __init__(self, parent):
		PyQt5.QtWidgets.QDoubleSpinBox.__init__(self, parent)
		self.setRange(-100, 100)
		self.setSuffix(self.tr('%', 'percent'))
		self.setButtonSymbols(PyQt5.QtWidgets.QAbstractSpinBox.PlusMinus)



# End.
