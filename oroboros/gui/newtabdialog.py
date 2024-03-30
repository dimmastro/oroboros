#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
New tab dialog.

"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHBoxLayout
import PyQt5


__all__ = ['NewTabDialog']



class NewTabDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		tr = self.tr
		self.setWindowTitle(tr('New Chart'))
		self.setSizeGripEnabled(True)
		# layout
		layout = PyQt5.QtWidgets.QVBoxLayout(self)
		self.setLayout(layout)
		# button group
		self.grpButtons = PyQt5.QtWidgets.QButtonGroup(self)
		# here-now button
		hereNowButton = PyQt5.QtWidgets.QRadioButton(tr('Here-Now Chart'), self)
		hereNowButton.setChecked(True)
		self.grpButtons.addButton(hereNowButton, 0)
		layout.addWidget(hereNowButton)
		# open chart
		openButton = PyQt5.QtWidgets.QRadioButton(tr('Open File'), self)
		self.grpButtons.addButton(openButton, 1)
		layout.addWidget(openButton)
		# custom chart
		customButton = PyQt5.QtWidgets.QRadioButton(tr('Custom Chart'), self)
		self.grpButtons.addButton(customButton, 2)
		layout.addWidget(customButton)
		# open astrolog32
		openA32Button = PyQt5.QtWidgets.QRadioButton(tr('Open Astrolog32'), self)
		self.grpButtons.addButton(openA32Button, 3)
		layout.addWidget(openA32Button)
		# open skif
		openSkifButton = PyQt5.QtWidgets.QRadioButton(tr('Open Skif'), self)
		self.grpButtons.addButton(openSkifButton, 4)
		layout.addWidget(openSkifButton)
		# dialog buttons
		bLayout = QHBoxLayout()
		layout.addLayout(bLayout)
		cancelButton = PyQt5.QtWidgets.QPushButton(tr('Cancel'), self)
		# self.connect(cancelButton, SIGNAL('clicked()'), self.reject)
		# bLayout.addWidget(cancelButton)
		cancelButton.clicked.connect(self.reject)

		okButton = PyQt5.QtWidgets.QPushButton(tr('OK'), self)
		okButton.setDefault(True)
		# self.connect(okButton, SIGNAL('clicked()'), self.accept)
		# bLayout.addWidget(okButton)
		okButton.clicked.connect(self.accept)

	def exec_(self):
		ok = PyQt5.QtWidgets.QDialog.exec_(self)
		if ok:
			return ok, self.grpButtons.checkedId()
		else:
			return ok, None
	
	

def main():
	import sys
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = NewTabDialog()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# End.
