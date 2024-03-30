#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Planets filters manager.

"""

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHBoxLayout

from oroboros.core.planetsfilters import PlanetsFilter, all_planets_filters_names
from oroboros.gui.plntfilterdialog import PlanetsFilterDialog
import PyQt5

__all__ = ['PlanetsFiltersManagerDialog']



class PlanetsFiltersManagerDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		self._parent = parent
		tr = self.tr
		self.setWindowTitle(tr('Planets Filters Manager'))
		self.setSizeGripEnabled(True)
		# layout
		grid = PyQt5.QtWidgets.QGridLayout(self)
		self.setLayout(grid)
		# list of filters
		self.filtersBox = PyQt5.QtWidgets.QComboBox(self)
		self.filtersBox.setEditable(False)
		self.filtersBox.addItems(all_planets_filters_names())
		grid.addWidget(self.filtersBox, 0, 0)
		# buttons
		buttonsLayout = QHBoxLayout()
		grid.addLayout(buttonsLayout, 1, 0)
		newButton = PyQt5.QtWidgets.QPushButton(tr('New'), self)
		# self.connect(newButton, SIGNAL('clicked()'), self.newFilterEvent)
		# buttonsLayout.addWidget(newButton)
		newButton.clicked.connect(self.newFilterEvent)

		editButton = PyQt5.QtWidgets.QPushButton(tr('Edit'), self)
		# self.connect(editButton, SIGNAL('clicked()'), self.editFilterEvent)
		# buttonsLayout.addWidget(editButton)
		editButton.clicked.connect(self.editFilterEvent)

		deleteButton = PyQt5.QtWidgets.QPushButton(tr('Delete'), self)
		# self.connect(deleteButton, SIGNAL('clicked()'), self.deleteFilterEvent)
		# buttonsLayout.addWidget(deleteButton)
		deleteButton.clicked.connect(self.deleteFilterEvent)

		closeButton = PyQt5.QtWidgets.QPushButton(tr('Close'), self)
		closeButton.setDefault(True)
		# self.connect(closeButton, SIGNAL('clicked()'), SLOT('close()'))
		# buttonsLayout.addWidget(closeButton)
		closeButton.clicked.connect(self.close)
	
	def newFilterEvent(self):
		new = PlanetsFilterDialog(self)
		ok = new.exec_()
		if ok:
			self.reset()
	
	def editFilterEvent(self):
		filt = PlanetsFilter(
			all_planets_filters_names()[self.filtersBox.currentIndex()])
		edit = PlanetsFilterDialog(self, filt)
		ok = edit.exec_()
		if ok:
			self.reset()
	
	def deleteFilterEvent(self):
		tr = self.tr
		name = all_planets_filters_names()[self.filtersBox.currentIndex()]
		ret = PyQt5.QtWidgets.QMessageBox.warning(self, tr('Delete Planets Filter'),
			str(tr('Are you sure you want to delete planets filter \xab %(filter)s \xbb ?')) % {
				'filter': name},
			PyQt5.QtWidgets.QMessageBox.Cancel|PyQt5.QtWidgets.QMessageBox.Yes, PyQt5.QtWidgets.QMessageBox.Yes)
		if ret == PyQt5.QtWidgets.QMessageBox.Yes:
			filt = PlanetsFilter(name)
			try:
				filt.delete()
			except ValueError: # cannot delete default filter
				PyQt5.QtWidgets.QMessageBox.critical(self, tr('Required Planets Filter'),
					tr('Cannot delete required filter.'))
			self.reset()
	
	def reset(self):
		"""Reload filters list."""
		self.filtersBox.clear()
		self.filtersBox.addItems(all_planets_filters_names())



def main():
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = PlanetsFiltersManagerDialog()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# End.
