#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
New/edit planets filters.

"""

import sys
import os.path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout

from oroboros.core import cfg
from oroboros.core import db
from oroboros.core.planetsfilters import PlanetsFilter

from oroboros.gui import app
from oroboros.gui import names
import PyQt5


__all__ = ['PlanetsFilterDialog']


_baseDir = os.path.dirname(os.path.abspath(__file__))



class PlanetsFilterDialog(PyQt5.QtWidgets.QDialog):
	
	def __init__(self, parent=None, filt=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		self._parent = parent
		tr = self.tr
		if isinstance(filt, PlanetsFilter):
			self._filt = filt
			title = str(tr('Edit Planets Filter \xab %(filter)s \xbb')) % {
				'filter': filt._name}
		else:
			self._filt = PlanetsFilter(cfg.dft_filter._planets._idx_)
			self._filt._idx_ = None # copy dft filter and set idx to None
			title = tr('New Planets Filter')
		self.setWindowTitle(title)
		# size
		self.setMinimumWidth(350)
		self.setMinimumHeight(350)
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
		
		# ### main planets ###
		mainWidget = QWidget()
		tabs.addTab(mainWidget, tr('Main', 'Main planets'))
		mainGrid = PyQt5.QtWidgets.QGridLayout()
		mainWidget.setLayout(mainGrid)
		# sun
		self._cb['Sun'] = PyQt5.QtWidgets.QCheckBox(names.planets['Sun'], self)
		mainGrid.addWidget(self._cb['Sun'], 0, 0)
		# moon
		self._cb['Moon'] = PyQt5.QtWidgets.QCheckBox(names.planets['Moon'], self)
		mainGrid.addWidget(self._cb['Moon'], 0, 1)
		# mercury
		self._cb['Mercury'] = PyQt5.QtWidgets.QCheckBox(names.planets['Mercury'], self)
		mainGrid.addWidget(self._cb['Mercury'], 0, 2)
		# venus
		self._cb['Venus'] = PyQt5.QtWidgets.QCheckBox(names.planets['Venus'], self)
		mainGrid.addWidget(self._cb['Venus'], 0, 3)
		# mars
		self._cb['Mars'] = PyQt5.QtWidgets.QCheckBox(names.planets['Mars'], self)
		mainGrid.addWidget(self._cb['Mars'], 0, 4)
		# jupiter
		self._cb['Jupiter'] = PyQt5.QtWidgets.QCheckBox(names.planets['Jupiter'], self)
		mainGrid.addWidget(self._cb['Jupiter'], 1, 0)
		# saturn
		self._cb['Saturn'] = PyQt5.QtWidgets.QCheckBox(names.planets['Saturn'], self)
		mainGrid.addWidget(self._cb['Saturn'], 1, 1)
		# uranus
		self._cb['Uranus'] = PyQt5.QtWidgets.QCheckBox(names.planets['Uranus'], self)
		mainGrid.addWidget(self._cb['Uranus'], 1, 2)
		# neptune
		self._cb['Neptune'] = PyQt5.QtWidgets.QCheckBox(names.planets['Neptune'], self)
		mainGrid.addWidget(self._cb['Neptune'], 1, 3)
		# pluto
		self._cb['Pluto'] = PyQt5.QtWidgets.QCheckBox(names.planets['Pluto'], self)
		mainGrid.addWidget(self._cb['Pluto'], 1, 4)
		# earth
		self._cb['Earth'] = PyQt5.QtWidgets.QCheckBox(names.planets['Earth'], self)
		mainGrid.addWidget(self._cb['Earth'], 2, 0)
		# chiron
		self._cb['Chiron'] = PyQt5.QtWidgets.QCheckBox(names.planets['Chiron'], self)
		mainGrid.addWidget(self._cb['Chiron'], 2, 1)
		# pholus
		self._cb['Pholus'] = PyQt5.QtWidgets.QCheckBox(names.planets['Pholus'], self)
		mainGrid.addWidget(self._cb['Pholus'], 2, 2)
		# ceres
		self._cb['Ceres'] = PyQt5.QtWidgets.QCheckBox(names.planets['Ceres'], self)
		mainGrid.addWidget(self._cb['Ceres'], 2, 3)
		# pallas
		self._cb['Pallas'] = PyQt5.QtWidgets.QCheckBox(names.planets['Pallas'], self)
		mainGrid.addWidget(self._cb['Pallas'], 2, 4)
		# juno
		self._cb['Juno'] = PyQt5.QtWidgets.QCheckBox(names.planets['Juno'], self)
		mainGrid.addWidget(self._cb['Juno'], 3, 0)
		# vesta
		self._cb['Vesta'] = PyQt5.QtWidgets.QCheckBox(names.planets['Vesta'], self)
		mainGrid.addWidget(self._cb['Vesta'], 3, 1)
		# rahu (mean)
		self._cb['Rahu (mean)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Rahu (mean)'], self)
		mainGrid.addWidget(self._cb['Rahu (mean)'], 3, 2)
		# rahu (true)
		self._cb['Rahu (true)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Rahu (true)'], self)
		mainGrid.addWidget(self._cb['Rahu (true)'], 3, 3)
		# ketu (mean)
		self._cb['Ketu (mean)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Ketu (mean)'], self)
		mainGrid.addWidget(self._cb['Ketu (mean)'], 3, 4)
		# ketu (true)
		self._cb['Ketu (true)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Ketu (true)'], self)
		mainGrid.addWidget(self._cb['Ketu (true)'], 4, 0)
		# lilith (mean)
		self._cb['Lilith (mean)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Lilith (mean)'], self)
		mainGrid.addWidget(self._cb['Lilith (mean)'], 4, 1)
		# lilith (true)
		self._cb['Lilith (true)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Lilith (true)'], self)
		mainGrid.addWidget(self._cb['Lilith (true)'], 4, 2)
		# priapus (mean)
		self._cb['Priapus (mean)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Priapus (mean)'], self)
		mainGrid.addWidget(self._cb['Priapus (mean)'], 4, 3)
		# priapus (true)
		self._cb['Priapus (true)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Priapus (true)'], self)
		mainGrid.addWidget(self._cb['Priapus (true)'], 4, 4)
		
		# ### uranians ###
		uranianWidget = QWidget()
		tabs.addTab(uranianWidget, tr('Uranians'))
		uranianGrid = PyQt5.QtWidgets.QGridLayout()
		uranianWidget.setLayout(uranianGrid)
		# cupido
		self._cb['Cupido'] = PyQt5.QtWidgets.QCheckBox(names.planets['Cupido'], self)
		uranianGrid.addWidget(self._cb['Cupido'], 0, 0)
		# hades
		self._cb['Hades'] = PyQt5.QtWidgets.QCheckBox(names.planets['Hades'], self)
		uranianGrid.addWidget(self._cb['Hades'], 0, 1)
		# zeus
		self._cb['Zeus'] = PyQt5.QtWidgets.QCheckBox(names.planets['Zeus'], self)
		uranianGrid.addWidget(self._cb['Zeus'], 0, 2)
		# kronos
		self._cb['Kronos'] = PyQt5.QtWidgets.QCheckBox(names.planets['Kronos'], self)
		uranianGrid.addWidget(self._cb['Kronos'], 0, 3)
		# apollo
		self._cb['Apollon'] = PyQt5.QtWidgets.QCheckBox(names.planets['Apollon'], self)
		uranianGrid.addWidget(self._cb['Apollon'], 1, 0)
		# admetos
		self._cb['Admetos'] = PyQt5.QtWidgets.QCheckBox(names.planets['Admetos'], self)
		uranianGrid.addWidget(self._cb['Admetos'], 1, 1)
		# vulkanus
		self._cb['Vulkanus'] = PyQt5.QtWidgets.QCheckBox(names.planets['Vulkanus'], self)
		uranianGrid.addWidget(self._cb['Vulkanus'], 1, 2)
		# poseidon
		self._cb['Poseidon'] = PyQt5.QtWidgets.QCheckBox(names.planets['Poseidon'], self)
		uranianGrid.addWidget(self._cb['Poseidon'], 1, 3)
		
		# ### others fictitious ###
		othersWidget = QWidget()
		tabs.addTab(othersWidget, tr('Others'))
		othersGrid = PyQt5.QtWidgets.QGridLayout()
		othersWidget.setLayout(othersGrid)
		# isis
		self._cb['Isis'] = PyQt5.QtWidgets.QCheckBox(names.planets['Isis'], self)
		othersGrid.addWidget(self._cb['Isis'], 0, 0)
		# nibiru
		self._cb['Nibiru'] = PyQt5.QtWidgets.QCheckBox(names.planets['Nibiru'], self)
		othersGrid.addWidget(self._cb['Nibiru'], 0, 1)
		# harrington
		self._cb['Harrington'] = PyQt5.QtWidgets.QCheckBox(names.planets['Harrington'], self)
		othersGrid.addWidget(self._cb['Harrington'], 0, 2)
		# neptune (leverrier)
		self._cb['Neptune (Leverrier)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Neptune (Leverrier)'], self)
		othersGrid.addWidget(self._cb['Neptune (Leverrier)'], 0, 3)
		# neptune (adams)
		self._cb['Neptune (Adams)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Neptune (Adams)'], self)
		othersGrid.addWidget(self._cb['Neptune (Adams)'], 1, 0)
		# pluto (lowell)
		self._cb['Pluto (Lowell)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Pluto (Lowell)'], self)
		othersGrid.addWidget(self._cb['Pluto (Lowell)'], 1, 1)
		# pluto (pickering)
		self._cb['Pluto (Pickering)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Pluto (Pickering)'], self)
		othersGrid.addWidget(self._cb['Pluto (Pickering)'], 1, 2)
		# vulcan
		self._cb['Vulcan'] = PyQt5.QtWidgets.QCheckBox(names.planets['Vulcan'], self)
		othersGrid.addWidget(self._cb['Vulcan'], 1, 3)
		# white moon
		self._cb['White Moon'] = PyQt5.QtWidgets.QCheckBox(names.planets['White Moon'], self)
		othersGrid.addWidget(self._cb['White Moon'], 2, 0)
		# proserpina
		self._cb['Proserpina'] = PyQt5.QtWidgets.QCheckBox(names.planets['Proserpina'], self)
		othersGrid.addWidget(self._cb['Proserpina'], 2, 1)
		# waldemath
		self._cb['Waldemath'] = PyQt5.QtWidgets.QCheckBox(names.planets['Waldemath'], self)
		othersGrid.addWidget(self._cb['Waldemath'], 2, 2)
		
		# ### cusps ###
		cuspsWidget = QWidget()
		tabs.addTab(cuspsWidget, tr('Cusps'))
		cuspsGrid = PyQt5.QtWidgets.QGridLayout()
		cuspsWidget.setLayout(cuspsGrid)
		# house cusps
		x = (0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2)
		y = (0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3)
		for i in range(12):
			self._cb['Cusp %.2d' % (i+1,)] = PyQt5.QtWidgets.QCheckBox(
				names.houses['Cusp %.2d' % (i+1,)], self)
			cuspsGrid.addWidget(self._cb['Cusp %.2d' % (i+1,)], x[i], y[i])
		# asc
		self._cb['Asc'] = PyQt5.QtWidgets.QCheckBox(names.planets['Asc'], self)
		cuspsGrid.addWidget(self._cb['Asc'], 3, 0)
		# mc
		self._cb['Mc'] = PyQt5.QtWidgets.QCheckBox(names.planets['Mc'], self)
		cuspsGrid.addWidget(self._cb['Mc'], 3, 1)
		# dsc
		self._cb['Dsc'] = PyQt5.QtWidgets.QCheckBox(names.planets['Dsc'], self)
		cuspsGrid.addWidget(self._cb['Dsc'], 3, 2)
		# ic
		self._cb['Ic'] = PyQt5.QtWidgets.QCheckBox(names.planets['Ic'], self)
		cuspsGrid.addWidget(self._cb['Ic'], 3, 3)
		# armc
		self._cb['Armc'] = PyQt5.QtWidgets.QCheckBox(names.planets['Armc'], self)
		cuspsGrid.addWidget(self._cb['Armc'], 4, 0)
		# vertex
		self._cb['Vertex'] = PyQt5.QtWidgets.QCheckBox(names.planets['Vertex'], self)
		cuspsGrid.addWidget(self._cb['Vertex'], 4, 1)
		# equatorial asc
		self._cb['Equatorial Ascendant'] = PyQt5.QtWidgets.QCheckBox(names.planets['Equatorial Ascendant'], self)
		cuspsGrid.addWidget(self._cb['Equatorial Ascendant'], 4, 2)
		# co-ascendant (koch)
		self._cb['Co-ascendant (Koch)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Co-ascendant (Koch)'], self)
		cuspsGrid.addWidget(self._cb['Co-ascendant (Koch)'], 4, 3)
		# co-ascendant (munkasey)
		self._cb['Co-ascendant (Munkasey)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Co-ascendant (Munkasey)'], self)
		cuspsGrid.addWidget(self._cb['Co-ascendant (Munkasey)'], 5, 0)
		# polar ascendant
		self._cb['Polar Ascendant (Munkasey)'] = PyQt5.QtWidgets.QCheckBox(names.planets['Polar Ascendant (Munkasey)'], self)
		cuspsGrid.addWidget(self._cb['Polar Ascendant (Munkasey)'], 5, 1)
		
		# ### gauquelin ###
		gauquelinWidget = QWidget()
		tabs.addTab(gauquelinWidget, tr('Gauquelin'))
		gauquelinGrid = PyQt5.QtWidgets.QGridLayout()
		gauquelinWidget.setLayout(gauquelinGrid)
		# sectors
		x = (0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,5)
		y = (0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5)
		for i in range(36):
			self._cb['Sector %.2d' % (i+1,)] = PyQt5.QtWidgets.QCheckBox(
				names.houses['Sector %.2d' % (i+1,)], self)
			gauquelinGrid.addWidget(self._cb['Sector %.2d' % (i+1,)], x[i], y[i])
		
		# ### parts ###
		partsWidget = QWidget()
		tabs.addTab(partsWidget, tr('Parts'))
		partsGrid = PyQt5.QtWidgets.QGridLayout()
		partsWidget.setLayout(partsGrid)
		# part of fortune (rudhyar)
		self._cb['Part of Fortune (Rudhyar)'] = PyQt5.QtWidgets.QCheckBox(
			names.planets['Part of Fortune (Rudhyar)'], self)
		partsGrid.addWidget(self._cb['Part of Fortune (Rudhyar)'], 0, 0)
		
		# ### fixed stars ###
		# get all stars
		sql = 'select name from Planets where family = 2 order by name;'
		res = db.execute(sql).fetchall()
		# stars tab
		starsScroll = PyQt5.QtWidgets.QScrollArea()
		starsScroll.setWidgetResizable(True)
		starsWidget = QWidget()
		starsScroll.setWidget(starsWidget)
		tabs.addTab(starsScroll, tr('Stars'))
		starsGrid = PyQt5.QtWidgets.QGridLayout()
		starsWidget.setLayout(starsGrid)
		y = 0
		for i, star in enumerate(res):
			s = str(star[0])
			self._cb[s] = PyQt5.QtWidgets.QCheckBox(s, self)
			starsGrid.addWidget(self._cb[s], y, i % 6)
			if i % 6 == 5:
				y += 1
		
		# ### asteroids ###
		# get all asteroids
		sql = 'select name from Planets where family = 3 order by name;'
		res = db.execute(sql).fetchall()
		# asteroids tab
		asteroidsScroll = PyQt5.QtWidgets.QScrollArea()
		asteroidsScroll.setWidgetResizable(True)
		asteroidsWidget = QWidget()
		asteroidsScroll.setWidget(asteroidsWidget)
		tabs.addTab(asteroidsScroll, tr('Asteroids'))
		asteroidsGrid = PyQt5.QtWidgets.QGridLayout()
		asteroidsWidget.setLayout(asteroidsGrid)
		y = 0
		for i, ast in enumerate(res):
			s = str(ast[0])
			self._cb[s] = PyQt5.QtWidgets.QCheckBox(s, self)
			asteroidsGrid.addWidget(self._cb[s], y, i % 6)
			if i % 6 == 5:
				y += 1
		
		# ### end planets ###
		
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
		for pl, val in self._filt.items():
				self._cb[pl].setChecked(val)
	
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
		for pl, cb in self._cb.items():
			self._filt[pl] = cb.isChecked()
		# save
		try:
			self._filt.save()
		except ValueError: # duplicate filter
			PyQt5.QtWidgets.QMessageBox.critical(self, tr('Error'),
				str(tr('Duplicate filter name \xab %(filter)s \xbb.')) % {
					'filter': self._filt._name})
			self.nameEdit.setFocus()
			return
		# reload cfg in case filter is default,
		# and opened charts if using this filter
		if __name__ != '__main__':
			app.planetsFilterUpdatedEvent(self._filt._idx_)
		# done
		self.done(PyQt5.QtWidgets.QDialog.Accepted)



def main():
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = PlanetsFilterDialog()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# End.
