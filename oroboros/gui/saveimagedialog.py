#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Save image dialog.

"""

import os.path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHBoxLayout

from oroboros.core import cfg
import PyQt5


__all__ = ['SaveImageDialog']


_iconsDir = os.path.join(os.path.dirname(__file__), 'icons')


class SaveImageDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		tr = self.tr
		self.setWindowTitle(tr('Save Image'))
		self.setSizeGripEnabled(True)
		self.setMinimumWidth(250)
		# layout
		grid = PyQt5.QtWidgets.QGridLayout(self)
		self.setLayout(grid)
		# file name
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('File Name')), 0, 0)
		self.fname = PyQt5.QtWidgets.QLineEdit(self)
		self.fname.setReadOnly(True)
		grid.addWidget(self.fname, 0, 1)
		# file chooser
		chooseButton = PyQt5.QtWidgets.QToolButton(self)
		chooseButton.setIcon(QIcon(os.path.join(_iconsDir, 'gtk-open.png')))
		chooseButton.setToolTip(tr('Get file name'))
		self.connect(chooseButton, SIGNAL('clicked()'), self.getFileName)
		grid.addWidget(chooseButton, 0, 2)
		# extension/format
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Extension')), 1, 0)
		self.extBox = PyQt5.QtWidgets.QComboBox(self)
		self.extBox.setEditable(False)
		self.extBox.addItems(
			['png', 'jpg', 'bmp', 'ppm', 'tiff', 'xbm', 'xpm', 'svg'])
		grid.addWidget(self.extBox, 1, 1, 1, 2)
		# width
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Width')), 2, 0)
		self.widthBox = PyQt5.QtWidgets.QSpinBox(self)
		self.widthBox.setRange(1, 10000)
		self.widthBox.setSuffix(tr('px', 'Pixels'))
		self.widthBox.setButtonSymbols(PyQt5.QtWidgets.QAbstractSpinBox.PlusMinus)
		self.widthBox.setValue(600)
		grid.addWidget(self.widthBox, 2, 1, 1, 2)
		# height
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Height')), 3, 0)
		self.heightBox = PyQt5.QtWidgets.QSpinBox(self)
		self.heightBox.setRange(1, 10000)
		self.heightBox.setSuffix(tr('px', 'Pixels'))
		self.heightBox.setButtonSymbols(PyQt5.QtWidgets.QAbstractSpinBox.PlusMinus)
		self.heightBox.setValue(600)
		grid.addWidget(self.heightBox, 3, 1, 1, 2)
		# buttons
		buttonsLayout = QHBoxLayout()
		grid.addLayout(buttonsLayout, 4, 0, 1, 3)
		cancelButton = PyQt5.QtWidgets.QPushButton(tr('Cancel'), self)
		self.connect(cancelButton, SIGNAL('clicked()'), self.reject)
		buttonsLayout.addWidget(cancelButton)
		okButton = PyQt5.QtWidgets.QPushButton(tr('Save'), self)
		okButton.setDefault(True)
		self.connect(okButton, SIGNAL('clicked()'), self.accept)
		buttonsLayout.addWidget(okButton)
	
	def getFileName(self):
		tr = self.tr
		path = unicode(QFileDialog.getSaveFileName(self,
			tr('Save Image As...'),
			os.path.expanduser(cfg.charts_dir),
			tr('Images (*.png *.jpg *.bmp *.ppm *.tiff *.xbm *.xpm *.svg)')))
		if path != '':
			self.fname.setText(path)
	
	def accept(self):
		"""Check input data."""
		if unicode(self.fname.text()) == '':
			PyQt5.QtWidgets.QMessageBox.critical(self, self.tr('Missing File Name'),
				self.tr('Please set file name.'))
			self.fname.setFocus()
			return
		else:
			PyQt5.QtWidgets.QDialog.accept(self)
	
	def exec_(self):
		ok = PyQt5.QtWidgets.QDialog.exec_(self)
		if not ok:
			return ok, None, None, None, None
		else:
			fname = unicode(self.fname.text())
			ext = unicode(self.extBox.currentText())
			w = self.widthBox.value()
			h = self.heightBox.value()
			return ok, fname, ext, w, h



def main():
	import sys
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = SaveImageDialog()
	main.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()

# End.
