#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filters manager.

"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHBoxLayout

from oroboros.core.filters import Filter, all_filters_names
from oroboros.gui.filterdialog import FilterDialog
import PyQt5

__all__ = ['FiltersManagerDialog']


class FiltersManagerDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None, mode='man'):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		self._parent = parent
		self._mode = mode # either 'man' or 'select'
		tr = self.tr
		self.setWindowTitle(tr('Filters Manager'))
		self.setSizeGripEnabled(True)
		# layout
		grid = PyQt5.QtWidgets.QGridLayout(self)
		self.setLayout(grid)
		# list of filters
		self.filtersBox = QComboBox(self)
		self.filtersBox.setEditable(False)
		self.filtersBox.addItems(all_filters_names())
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
		if mode == 'man':
			closeButton = PyQt5.QtWidgets.QPushButton(tr('Close'), self)
			self.connect(closeButton, SIGNAL('clicked()'), SLOT('close()'))
		elif mode == 'select':
			closeButton = PyQt5.QtWidgets.QPushButton(tr('Select'), self)
			self.connect(closeButton, SIGNAL('clicked()'), self.accept)
		closeButton.setDefault(True)
		buttonsLayout.addWidget(closeButton)
	
	def newFilterEvent(self):
		new = FilterDialog(self)
		ok = new.exec_()
		if ok:
			self.reset()
	
	def editFilterEvent(self):
		filt = Filter(all_filters_names()[self.filtersBox.currentIndex()])
		edit = FilterDialog(self, filt)
		ok = edit.exec_()
		if ok:
			self.reset()
	
	def deleteFilterEvent(self):
		tr = self.tr
		name = all_filters_names()[self.filtersBox.currentIndex()]
		ret = PyQt5.QtWidgets.QMessageBox.warning(self, tr('Delete Filter'),
			str(tr('Are you sure you want to delete filter \xab %(filter)s \xbb ?')) % {
				'filter': name},
			PyQt5.QtWidgets.QMessageBox.Cancel|PyQt5.QtWidgets.QMessageBox.Yes, PyQt5.QtWidgets.QMessageBox.Yes)
		if ret == PyQt5.QtWidgets.QMessageBox.Yes:
			filt = Filter(name)
			try:
				filt.delete()
			except ValueError: # cannot delete
				PyQt5.QtWidgets.QMessageBox.critical(self, tr('Default Filter'),
					tr('Cannot delete default filter.'))
			self.reset()
	
	def reset(self):
		"""Reload filters list."""
		self.filtersBox.clear()
		self.filtersBox.addItems(all_filters_names())
	
	def exec_(self):
		if self._mode == 'select':
			ok = PyQt5.QtWidgets.QDialog.exec_(self)
			if ok:
				name = all_filters_names()[self.filtersBox.currentIndex()]
				return ok, name
			else:
				return ok, None
		else:
			return PyQt5.QtWidgets.QDialog.exec_(self)



def main():
	import sys
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = FiltersManagerDialog()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# End.
