#!/sur/bin/env python
# -*- coding: utf8 -*-

"""
Multiply/profection dialog.

"""

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHBoxLayout
import PyQt5

__all__ = ['HarmonicsDialog']


class HarmonicsDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		tr = self.tr
		self.setWindowTitle(tr('Multiply Degrees'))
		layout = PyQt5.QtWidgets.QGridLayout(self)
		self.setLayout(layout)
		# input value
		layout.addWidget(PyQt5.QtWidgets.QLabel(tr('Value')), 0, 0)
		self.valueEdit = PyQt5.QtWidgets.QDoubleSpinBox(self)
		self.valueEdit.setRange(0, 360)
		self.valueEdit.setSuffix(tr('\xb0', 'Degrees'))
		self.valueEdit.setDecimals(6)
		self.valueEdit.setButtonSymbols(QAbstractSpinBox.PlusMinus)
		self.valueEdit.setValue(2)
		layout.addWidget(self.valueEdit, 0, 1)
		# profection mode
		self.profMode = QCheckBox(tr('Profection'), self)
		self.connect(self.profMode, SIGNAL('stateChanged(int)'),
			self.setProfMode)
		layout.addWidget(self.profMode, 1, 0)
		# profection unit
		self.profUnit = QComboBox(self)
		self.profUnit.setEditable(False)
		self.profUnit.setDisabled(True)
		units = [tr('Per year'), tr('Per day'), tr('Per hour')]
		self.profUnit.addItems(units)
		layout.addWidget(self.profUnit, 1, 1)
		# datetime
		layout.addWidget(PyQt5.QtWidgets.QLabel(tr('DateTime')), 2, 0)
		self.datetimeEdit = QDateTimeEdit(QDateTime.currentDateTime(), self)
		self.datetimeEdit.setCalendarPopup(True)
		self.datetimeEdit.setDisplayFormat(tr('yyyy-MM-dd hh:mm:ss',
			'Datetime format'))
		self.datetimeEdit.setMinimumDateTime(QDateTime(-5400, 1, 1, 0, 0))
		self.datetimeEdit.setMaximumDateTime(QDateTime(5400, 1, 1, 0, 0))
		self.datetimeEdit.setButtonSymbols(QAbstractSpinBox.PlusMinus)
		self.datetimeEdit.setDisabled(True)
		layout.addWidget(self.datetimeEdit, 2, 1)
		# buttons
		buttonsLayout = QHBoxLayout()
		layout.addLayout(buttonsLayout, 3, 0, 1, 2)
		cancelButton = PyQt5.QtWidgets.QPushButton(tr('Cancel'), self)
		self.connect(cancelButton, SIGNAL('clicked()'), self.reject)
		buttonsLayout.addWidget(cancelButton)
		okButton = PyQt5.QtWidgets.QPushButton(tr('Ok'), self)
		okButton.setDefault(True)
		self.connect(okButton, SIGNAL('clicked()'), self.accept)
		buttonsLayout.addWidget(okButton)
	
	def setProfMode(self, i):
		"""Enable/disable profection."""
		if self.profMode.isChecked():
			self.profUnit.setEnabled(True)
			self.datetimeEdit.setEnabled(True)
		else:
			self.profUnit.setDisabled(True)
			self.datetimeEdit.setDisabled(True)
	
	def exec_(self):
		"""Return ok, value, profection, profection unit, datetime."""
		ok = PyQt5.QtWidgets.QDialog.exec_(self)
		if ok:
			ret = (PyQt5.QtWidgets.QDialog.Accepted, self.valueEdit.value(),
				self.profMode.isChecked(), self.profUnit.currentIndex(),
				self.datetimeEdit.dateTime().toPyDateTime())
			return ret
		else:
			return PyQt5.QtWidgets.QDialog.Rejected, 0, False, -1, 0



def main():
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = HarmonicsDialog()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# End.
