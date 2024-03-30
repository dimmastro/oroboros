#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mid-points filters manager.

"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHBoxLayout

from oroboros.core.midpfilters import MidPointsFilter, all_midpoints_filters_names
from oroboros.gui.midpfilterdialog import MidPointsFilterDialog
import PyQt5

__all__ = ['MidPointsFiltersManagerDialog']



class MidPointsFiltersManagerDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		self._parent = parent
		tr = self.tr
		self.setWindowTitle(tr('MidPoints Filters Manager'))
		self.setSizeGripEnabled(True)
		# layout
		grid = PyQt5.QtWidgets.QGridLayout(self)
		self.setLayout(grid)
		# list of filters
		self.filtersBox = QComboBox(self)
		self.filtersBox.setEditable(False)
		self.filtersBox.addItems(all_midpoints_filters_names())
		grid.addWidget(self.filtersBox, 0, 0)
		# buttons
		buttonsLayout = QHBoxLayout()
		grid.addLayout(buttonsLayout, 1, 0)
		newButton = PyQt5.QtWidgets.QPushButton(tr('New'), self)
		self.connect(newButton, SIGNAL('clicked()'), self.newFilterEvent)
		buttonsLayout.addWidget(newButton)
		editButton = PyQt5.QtWidgets.QPushButton(tr('Edit'), self)
		self.connect(editButton, SIGNAL('clicked()'), self.editFilterEvent)
		buttonsLayout.addWidget(editButton)
		deleteButton = PyQt5.QtWidgets.QPushButton(tr('Delete'), self)
		self.connect(deleteButton, SIGNAL('clicked()'), self.deleteFilterEvent)
		buttonsLayout.addWidget(deleteButton)
		closeButton = PyQt5.QtWidgets.QPushButton(tr('Close'), self)
		closeButton.setDefault(True)
		self.connect(closeButton, SIGNAL('clicked()'), SLOT('close()'))
		buttonsLayout.addWidget(closeButton)
	
	def newFilterEvent(self):
		new = MidPointsFilterDialog(self)
		ok = new.exec_()
		if ok:
			self.reset()
	
	def editFilterEvent(self):
		filt = MidPointsFilter(
			all_midpoints_filters_names()[self.filtersBox.currentIndex()])
		edit = MidPointsFilterDialog(self, filt)
		ok = edit.exec_()
		if ok:
			self.reset()
	
	def deleteFilterEvent(self):
		tr = self.tr
		name = all_midpoints_filters_names()[self.filtersBox.currentIndex()]
		ret = PyQt5.QtWidgets.QMessageBox.warning(self, tr('Delete MidPoints Filter'),
			str(tr('Are you sure you want to delete mid-points filter \xab %(filter)s \xbb ?')) % {
				'filter': name},
			PyQt5.QtWidgets.QMessageBox.Cancel|PyQt5.QtWidgets.QMessageBox.Yes, PyQt5.QtWidgets.QMessageBox.Yes)
		if ret == PyQt5.QtWidgets.QMessageBox.Yes:
			filt = MidPointsFilter(name)
			try:
				filt.delete()
			except ValueError: # cannot delete default filter
				PyQt5.QtWidgets.QMessageBox.critical(self, tr('Default MidPoints Filter'),
					tr('Cannot delete filter used as default.'))
			self.reset()
	
	def reset(self):
		"""Reload filters list."""
		self.filtersBox.clear()
		self.filtersBox.addItems(all_midpoints_filters_names())



def main():
	import sys
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = MidPointsFiltersManagerDialog()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# End.
