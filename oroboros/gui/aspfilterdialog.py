#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
New/edit aspects filters.

"""

import sys
import os.path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout

from oroboros.core import cfg
from oroboros.core.filters import all_filters_names
from oroboros.core.aspectsfilters import AspectsFilter

from oroboros.gui import app
from oroboros.gui import names
import PyQt5


__all__ = ['AspectsFilterDialog']


_baseDir = os.path.dirname(os.path.abspath(__file__))


class AspectsFilterDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None, filt=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		self._parent = parent
		tr = self.tr
		if isinstance(filt, AspectsFilter):
			self._filt = filt
			title = str(tr('Edit Aspects Filter \xab %(filter)s \xbb')) % {
				'filter': filt._name}
		else:
			self._filt = AspectsFilter(cfg.dft_filter._aspects._idx_)
			self._filt._idx_ = None # copy dft filter and set idx to None
			title = tr('New Aspects Filter')
		self.setWindowTitle(title)
		# size
		self.setMinimumWidth(350)
		self.setMinimumHeight(320)
		self.setSizeGripEnabled(True)
		# layout
		grid = PyQt5.QtWidgets.QGridLayout(self)
		self.setLayout(grid)
		# filter name
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Filter name')), 0, 0)
		self.nameEdit = PyQt5.QtWidgets.QLineEdit(self)
		grid.addWidget(self.nameEdit, 0, 1)
		# tab widget
		tabs = QTabWidget(self)
		grid.addWidget(tabs, 1, 0, 1, 2)
		self._cb = dict() ## holds the checkboxes
		
		# ### main aspects ###
		mainWidget = QWidget()
		tabs.addTab(mainWidget, tr('Main', 'Main aspects'))
		mainGrid = PyQt5.QtWidgets.QGridLayout()
		mainWidget.setLayout(mainGrid)
		x = (0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3)
		y = (0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3)
		mainAspects = ('Conjunction', 'Opposition', 'Trine', 'Square', 'Sextile',
			'Quincunx', 'SesquiSquare', 'SemiSquare', 'SemiSextile', 'SquiSquare',
			'SquiSextile', 'Quintile', 'BiQuintile', 'SemiQuintile')
		for i, asp in enumerate(mainAspects):
			self._cb[asp] = PyQt5.QtWidgets.QCheckBox(names.aspects[asp], self)
			mainGrid.addWidget(self._cb[asp], x[i], y[i])
		
		# ### other aspects ###$
		otherWidget = QWidget()
		tabs.addTab(otherWidget, tr('Others', 'Other aspects'))
		otherGrid = PyQt5.QtWidgets.QGridLayout()
		otherWidget.setLayout(otherGrid)
		x = (0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3)
		y = (0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3)
		otherAspects = ('Novile', 'BiNovile', 'QuadriNovile', 'SemiNovile',
			'Septile', 'BiSeptile', 'TriSeptile', 'Undecile', 'BiUndecile',
			'TriUndecile', 'QuadUndecile', 'QuinUndecile')
		for i, asp in enumerate(otherAspects):
			self._cb[asp] = PyQt5.QtWidgets.QCheckBox(names.aspects[asp], self)
			otherGrid.addWidget(self._cb[asp], x[i], y[i])
		
		# comment
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Comment')), 2, 0, Qt.AlignTop)
		self.commentEdit = PyQt5.QtWidgets.QTextEdit('', self)
		grid.addWidget(self.commentEdit, 2, 1)
		# buttons
		buttonsLayout = QHBoxLayout()
		resetButton = PyQt5.QtWidgets.QPushButton(tr('Reset'), self)
		self.connect(resetButton, SIGNAL('clicked()'), self.reset)
		buttonsLayout.addWidget(resetButton)
		cancelButton = PyQt5.QtWidgets.QPushButton(tr('Cancel'), self)
		self.connect(cancelButton, SIGNAL('clicked()'), self.reject)
		buttonsLayout.addWidget(cancelButton)
		okButton = PyQt5.QtWidgets.QPushButton(tr('Ok'), self)
		okButton.setDefault(True)
		self.connect(okButton, SIGNAL('clicked()'), self.accept)
		buttonsLayout.addWidget(okButton)
		grid.addLayout(buttonsLayout, 3, 0, 1, 2)
		# load entries
		self.reset()
		# resize
		self.resize(550, 300)
	
	def reset(self):
		"""Reset entries."""
		# name
		self.nameEdit.setText(self._filt._name)
		# comment
		self.commentEdit.setPlainText(self._filt._comment)
		# values
		for asp, val in self._filt.items():
				self._cb[asp].setChecked(val)
	
	def accept(self):
		"""Set filter new values and save."""
		tr = self.tr
		# name
		name = unicode(self.nameEdit.text())
		if name == '':
			PyQt5.QtWidgets.QMessageBox.critical(self, tr('Missing Name'),
				tr('Please set filter name.'))
			self.nameEdit.setFocus()
			return
		# comment
		cmt = unicode(self.commentEdit.toPlainText())
		# set values
		self._filt.set(name=name, comment=cmt)
		for asp, cb in self._cb.items():
			self._filt[asp] = cb.isChecked()
		# save
		try:
			self._filt.save()
		except ValueError: # duplicate filter
			PyQt5.QtWidgets.QMessageBox.critical(self, tr('Error'),
				str(tr('Duplicate filter name \xab %s \xbb.')) % self._filt._name)
			self.nameEdit.setFocus()
			return
		# reload cfg in case filter is default,
		# and opened charts if using this filter
		if __name__ != '__main__':
			app.aspectsFilterUpdatedEvent(self._filt._idx_)
		# done
		self.done(PyQt5.QtWidgets.QDialog.Accepted)



def main():
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = AspectsFilterDialog()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# End.
