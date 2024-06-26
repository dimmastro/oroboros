#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
New/edit orbs filters.

"""

import sys
import os.path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout


from oroboros.core import cfg
from oroboros.core.orbsfilters import OrbsFilter

from oroboros.gui import app
from oroboros.gui import names
import PyQt5


__all__ = ['OrbsFilterDialog']


_baseDir = os.path.dirname(os.path.abspath(__file__))



class OrbsFilterDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None, filt=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		self._parent = parent
		tr = self.tr
		if isinstance(filt, OrbsFilter):
			self._filt = filt
			title = str(tr('Edit Orbs Filter \xab %(filter)s \xbb')) % {
				'filter': filt._name}
		else:
			self._filt = OrbsFilter(cfg.dft_filter._orbs._idx_)
			self._filt._idx_ = None # copy dft filter and set idx to None
			title = tr('New Orbs Filter')
		self.setWindowTitle(title)
		# size
		self.setMinimumWidth(500)
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
		self._sb = dict() ## holds the spinboxes
		
		# ### main aspects ###
		mainWidget = QWidget()
		tabs.addTab(mainWidget, tr('Main', 'Main aspects'))
		mainGrid = PyQt5.QtWidgets.QGridLayout()
		mainWidget.setLayout(mainGrid)
		x = (0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3)
		y = (0,2,4,6,0,2,4,6,0,2,4,6,0,2,4,6)
		mainAspects = ('Conjunction', 'Opposition', 'Trine', 'Square', 'Sextile',
			'Quincunx', 'SesquiSquare', 'SemiSquare', 'SemiSextile', 'SquiSquare',
			'SquiSextile', 'Quintile', 'BiQuintile', 'SemiQuintile')
		for i, asp in enumerate(mainAspects):
			mainGrid.addWidget(PyQt5.QtWidgets.QLabel(names.aspects[asp]), x[i], y[i])
			self._sb[asp] = PyQt5.QtWidgets.QDoubleSpinBox(self)
			self._sb[asp].setRange(0, 30)
			self._sb[asp].setButtonSymbols(PyQt5.QtWidgets.QAbstractSpinBox.PlusMinus)
			self._sb[asp].setSuffix(tr('\xb0', 'Degrees'))
			mainGrid.addWidget(self._sb[asp], x[i], y[i]+1)
		
		# ### other aspects ###
		otherWidget = QWidget()
		tabs.addTab(otherWidget, tr('Others', 'Other aspects'))
		otherGrid = PyQt5.QtWidgets.QGridLayout()
		otherWidget.setLayout(otherGrid)
		x = (0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3)
		y = (0,2,4,6,0,2,4,6,0,2,4,6,0,2,4,6)
		otherAspects = ('Novile', 'BiNovile', 'QuadriNovile', 'SemiNovile',
			'Septile', 'BiSeptile', 'TriSeptile', 'Undecile', 'BiUndecile',
			'TriUndecile', 'QuadUndecile', 'QuinUndecile')
		for i, asp in enumerate(otherAspects):
			otherGrid.addWidget(PyQt5.QtWidgets.QLabel(names.aspects[asp]), x[i], y[i])
			self._sb[asp] = PyQt5.QtWidgets.QDoubleSpinBox(self)
			self._sb[asp].setRange(0, 30)
			self._sb[asp].setButtonSymbols(PyQt5.QtWidgets.QAbstractSpinBox.PlusMinus)
			self._sb[asp].setSuffix(tr('\xb0', 'Degrees'))
			otherGrid.addWidget(self._sb[asp], x[i], y[i]+1)
		
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
				self._sb[asp].setValue(val)
	
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
		for asp, sb in self._sb.items():
			self._filt[asp] = sb.value()
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
			app.orbsFilterUpdatedEvent(self._filt._idx_)
		# done
		self.done(PyQt5.QtWidgets.QDialog.Accepted)



def main():
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = OrbsFilterDialog()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# End.
