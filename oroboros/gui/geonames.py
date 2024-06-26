#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GeoNames.org query interface.

"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHBoxLayout
import PyQt5

from oroboros.core import geonames


__all__ = ['GeoNamesQueryDialog']


class GeoNamesQueryDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		tr = self.tr
		self._parent = parent
		self.setWindowTitle(tr('Query GeoNames.org'))
		self.setSizeGripEnabled(True)
		self.setMinimumWidth(400)
		self._results = list() # geonames results
		self._sel = None # selected result
		# layout
		grid = PyQt5.QtWidgets.QGridLayout(self)
		self.setLayout(grid)
		# search
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Search for')), 0, 0)
		self.nameQuery = PyQt5.QtWidgets.QLineEdit(self)
		grid.addWidget(self.nameQuery, 0, 1)
		# results
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Results')), 1, 0)
		self.resultsBox = PyQt5.QtWidgets.QComboBox(self)
		self.resultsBox.setEditable(False)
		grid.addWidget(self.resultsBox, 1, 1)
		# buttons
		buttonsLayout = QHBoxLayout()
		grid.addLayout(buttonsLayout, 2, 0, 1, 2)
		searchButton = PyQt5.QtWidgets.QPushButton(tr('Search'), self)
		searchButton.setDefault(True)
		self.connect(searchButton, SIGNAL('clicked()'), self.searchEvent)
		buttonsLayout.addWidget(searchButton)
		self.selectButton = PyQt5.QtWidgets.QPushButton(tr('Select'), self)
		self.selectButton.setDisabled(True)
		self.connect(self.selectButton, SIGNAL('clicked()'), self.selectEvent)
		buttonsLayout.addWidget(self.selectButton)
		closeButton = PyQt5.QtWidgets.QPushButton(tr('Close'), self)
		self.connect(closeButton, SIGNAL('clicked()'), SLOT('close()'))
		buttonsLayout.addWidget(closeButton)
	
	def searchEvent(self):
		tr = self.tr
		txt = unicode(self.nameQuery.text()).strip()
		if txt == '': # no input
			self.selectButton.setDisabled(True)
			self.nameQuery.setFocus()
			return
		# threading
		th = SearchThread(txt, self)
		progDialog = ProgressDialog(self)
		self.connect(th, SIGNAL('finished()'), progDialog, SLOT('accept()'))
		self.connect(th, SIGNAL('terminated()'), progDialog, SLOT('reject()'))
		self.connect(progDialog, SIGNAL('rejected()'), th, SLOT('quit()'))
		th.start()
		ok = progDialog.exec_()
		if not ok: # aborted or error
			return
		# display results
		fmt = unicode(
			tr('%(name)s, %(cty)s, %(lat)s, %(lon)s, %(alt)s %(m)s, %(tz)s'))
		all = [fmt % {
			'name': x[0], 
			'cty': x[1],
			'lat': str(x[2]),
			'lon': str(x[3]),
			'alt': str(x[4]),
			'm': tr('m.', 'Meters'),
			'tz': x[5]
			}	for x in self._results]
		self.resultsBox.clear()
		if len(all) != 0:
			self.resultsBox.addItems(all)
			self.selectButton.setEnabled(True)
		else:
			self.selectButton.setDisabled(True)
	
	def selectEvent(self):
		"""Set parent's geonames results."""
		try:
			self._sel = self._results[self.resultsBox.currentIndex()]
		except IndexError: # should not happen
			self.done(PyQt5.QtWidgets.QDialog.Rejected)
		self.done(PyQt5.QtWidgets.QDialog.Accepted)
	
	def exec_(self):
		ok = PyQt5.QtWidgets.QDialog.exec_(self)
		if ok:
			return ok, self._sel
		else:
			return ok, None


class SearchThread(QThread):
	"""Query geonames.org in a thread."""
	
	def __init__(self, txt, parent):
		QThread.__init__(self, parent)
		self._parent = parent
		self._txt = txt.encode('utf-8')
	
	def run(self):
		try:
			self._parent._results = geonames.search(self._txt)
		except ValueError: # not connected?
			#raise
			self.terminate()##self.emit(SIGNAL('terminated()'))


class ProgressDialog(PyQt5.QtWidgets.QSpinBox):
	"""Progress bar dialog."""
	
	def __init__(self, parent):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		self.setWindowTitle(self.tr('Waiting...', 'Progress bar'))
		layout = QHBoxLayout(self)
		self.setLayout(layout)
		progBar = QProgressBar(self)
		progBar.setRange(0, 0)
		layout.addWidget(progBar)



def main():
	import sys
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = GeoNamesQueryDialog()
	main.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()

# End.
