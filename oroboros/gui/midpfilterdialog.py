#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
New/edit mid-points filter.

"""

import sys
import os.path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHBoxLayout

from oroboros.core import cfg
from oroboros.core.midpfilters import MidPointsFilter
from oroboros.core.planetsfilters import PlanetsFilter, all_planets_filters_names
from oroboros.core.aspectsfilters import AspectsFilter, all_aspects_filters_names
from oroboros.core.orbsfilters import OrbsFilter, all_orbs_filters_names
from oroboros.core.aspectsrestrictions import AspectsRestrictions, all_aspects_restrictions_names
from oroboros.core.orbsrestrictions import OrbsRestrictions, all_orbs_restrictions_names

from oroboros.gui import app
from oroboros.gui.plntfilterdialog import PlanetsFilterDialog
from oroboros.gui.aspfilterdialog import AspectsFilterDialog
from oroboros.gui.orbfilterdialog import OrbsFilterDialog
from oroboros.gui.asprestrdialog import AspectsRestrictionsDialog
from oroboros.gui.orbrestrdialog import OrbsRestrictionsDialog
import PyQt5

__all__ = ['MidPointsFilterDialog']


_baseDir = os.path.dirname(os.path.abspath(__file__))


class MidPointsFilterDialog(PyQt5.QtWidgets.QDialog):
	"""Mid-points filter settings."""
	
	def __init__(self, parent=None, filt=None):
		PyQt5.QtWidgets.QDialog.__init__(self, parent)
		self._parent = parent
		tr = self.tr
		if isinstance(filt, MidPointsFilter):
			self._filt = filt
			title = str(tr('Edit MidPoints Filter \xab %(filter)s \xbb')) % {
				'filter': filt._name}
		else:
			self._filt = MidPointsFilter(cfg.dft_filter._midpoints._idx_)
			self._filt._idx_ = None # copy dft filter and set idx to None
			title = tr('New MidPoints Filter')
		self.setWindowTitle(title)
		# size
		self.setMinimumWidth(300)
		self.setMaximumHeight(300)
		self.setSizeGripEnabled(True)
		# layout
		grid = PyQt5.QtWidgets.QGridLayout(self)
		self.setLayout(grid)
		# filter name
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Filter name')), 0, 0)
		self.nameEdit = PyQt5.QtWidgets.QLineEdit(self)
		grid.addWidget(self.nameEdit, 0, 1)
		# midp planets filter
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Planets filter')), 1, 0)
		mppfLayout = QHBoxLayout()
		self.planetsEdit = PyQt5.QtWidgets.QComboBox(self)
		self.planetsEdit.setEditable(False)
		mppfLayout.addWidget(self.planetsEdit)
		mppfButton = PyQt5.QtWidgets.QToolButton(self)
		mppfButton.setIcon(QIcon(os.path.join(_baseDir, 'icons',
			'gtk-execute.png')))
		mppfButton.setToolTip(tr('Edit planets filter'))
		self.connect(mppfButton, SIGNAL('clicked()'), self.editPlanetsFilter)
		mppfLayout.addWidget(mppfButton)
		grid.addLayout(mppfLayout, 1, 1)
		# midp aspects filter
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Aspects filter')), 2, 0)
		mpafLayout = QHBoxLayout()
		self.aspectsEdit = PyQt5.QtWidgets.QComboBox(self)
		self.aspectsEdit.setEditable(False)
		mpafLayout.addWidget(self.aspectsEdit)
		mpafButton = PyQt5.QtWidgets.QToolButton(self)
		mpafButton.setIcon(QIcon(os.path.join(_baseDir, 'icons',
			'gtk-execute.png')))
		mpafButton.setToolTip(tr('Edit aspects filter'))
		self.connect(mpafButton, SIGNAL('clicked()'), self.editAspectsFilter)
		mpafLayout.addWidget(mpafButton)
		grid.addLayout(mpafLayout, 2, 1)
		# midp orbs filter
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Orbs filter')), 3, 0)
		mpofLayout = QHBoxLayout()
		self.orbsEdit = PyQt5.QtWidgets.QComboBox(self)
		self.orbsEdit.setEditable(False)
		mpofLayout.addWidget(self.orbsEdit)
		mpofButton = PyQt5.QtWidgets.QToolButton(self)
		mpofButton.setIcon(QIcon(os.path.join(_baseDir, 'icons',
			'gtk-execute.png')))
		mpofButton.setToolTip(tr('Edit orbs filter'))
		self.connect(mpofButton, SIGNAL('clicked()'), self.editOrbsFilter)
		mpofLayout.addWidget(mpofButton)
		grid.addLayout(mpofLayout, 3, 1)
		# midp aspects restrictions
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Aspects restrictions')), 4, 0)
		mparLayout = QHBoxLayout()
		self.asprestrEdit = PyQt5.QtWidgets.QComboBox(self)
		self.asprestrEdit.setEditable(False)
		mparLayout.addWidget(self.asprestrEdit)
		mparButton = PyQt5.QtWidgets.QToolButton(self)
		mparButton.setIcon(QIcon(os.path.join(_baseDir, 'icons',
			'gtk-execute.png')))
		mparButton.setToolTip(tr('Edit aspects restrictions'))
		self.connect(mparButton, SIGNAL('clicked()'), self.editAspectsRestrictions)
		mparLayout.addWidget(mparButton)
		grid.addLayout(mparLayout, 4, 1)
		# midp orbs restrictions
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Orbs modifiers')), 5, 0)
		mporLayout = QHBoxLayout()
		self.orbrestrEdit = PyQt5.QtWidgets.QComboBox(self)
		self.orbrestrEdit.setEditable(False)
		mporLayout.addWidget(self.orbrestrEdit)
		mporButton = PyQt5.QtWidgets.QToolButton(self)
		mporButton.setIcon(QIcon(os.path.join(_baseDir, 'icons',
			'gtk-execute.png')))
		mporButton.setToolTip(tr('Edit orbs restrictions'))
		self.connect(mporButton, SIGNAL('clicked()'), self.editOrbsRestrictions)
		mporLayout.addWidget(mporButton)
		grid.addLayout(mporLayout, 5, 1)
		# comment
		grid.addWidget(PyQt5.QtWidgets.QLabel(tr('Comment')), 6, 0, Qt.AlignTop)
		self.commentEdit = QTextEdit('', self)
		grid.addWidget(self.commentEdit, 6, 1)
		
		# ### buttons ###
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
		grid.addLayout(buttonsLayout, 7, 0, 1, 2)
		# load entries
		self.reset()
	
	
	# ### edit midpoints filters ###
	
	def editPlanetsFilter(self):
		"""Open planets filter edit dialog."""
		pf = PlanetsFilter(
			all_planets_filters_names()[self.planetsEdit.currentIndex()])
		edit = PlanetsFilterDialog(self, pf)
		ok = edit.exec_()
		if ok: ## reset our filters
			if pf == self._filt._planets:
				self._filt._planets.reset()
			self.resetPlanetsFilters()
	
	def editAspectsFilter(self):
		"""Open aspects filter edit dialog."""
		af = AspectsFilter(
			all_aspects_filters_names()[self.aspectsEdit.currentIndex()])
		edit = AspectsFilterDialog(self, af)
		ok = edit.exec_()
		if ok: ## reset our filters
			if af == self._filt._aspects:
				self._filt._aspects.reset()
			self.resetAspectsFilters()
	
	def editOrbsFilter(self):
		of = OrbsFilter(
			all_orbs_filters_names()[self.orbsEdit.currentIndex()])
		edit = OrbsFilterDialog(self, of)
		ok = edit.exec_()
		if ok: ## reset our filters
			if of == self._filt._orbs:
				self._filt._orbs.reset()
			self.resetOrbsFilters()
	
	def editAspectsRestrictions(self):
		ar = AspectsRestrictions(
			all_aspects_restrictions_names()[self.asprestrEdit.currentIndex()])
		edit = AspectsRestrictionsDialog(self, ar)
		ok = edit.exec_()
		if ok: ## reset our filters
			if ar == self._filt._asprestr:
				self._filt._asprestr.reset()
			self.resetAspectsRestrictions()
	
	def editOrbsRestrictions(self):
		orb = OrbsRestrictions(
			all_orbs_restrictions_names()[self.orbrestrEdit.currentIndex()])
		edit = OrbsRestrictionsDialog(self, orb)
		ok = edit.exec_()
		if ok: ## reset our filters
			if orb == self._filt._orbrestr:
				self._filt._orbrestr.reset()
			self.resetOrbsRestrictions()
	
	# ### reset filters boxes ###
	
	def resetPlanetsFilters(self):
		"""Reset planets filter box."""
		self.planetsEdit.clear()
		all = all_planets_filters_names()
		self.planetsEdit.addItems(all)
		i = all.index(self._filt._planets._name)
		self.planetsEdit.setCurrentIndex(i)
	
	def resetAspectsFilters(self):
		"""Reset aspects filters box."""
		self.aspectsEdit.clear()
		all = all_aspects_filters_names()
		self.aspectsEdit.addItems(all)
		i = all.index(self._filt._aspects._name)
		self.aspectsEdit.setCurrentIndex(i)
	
	def resetOrbsFilters(self):
		"""Reset orbs filters box."""
		self.orbsEdit.clear()
		all = all_orbs_filters_names()
		self.orbsEdit.addItems(all)
		i = all.index(self._filt._orbs._name)
		self.orbsEdit.setCurrentIndex(i)
	
	def resetAspectsRestrictions(self):
		"""Reset aspects restrictions box."""
		self.asprestrEdit.clear()
		all = all_aspects_restrictions_names()
		self.asprestrEdit.addItems(all)
		i = all.index(self._filt._asprestr._name)
	
	def resetOrbsRestrictions(self):
		"""Reset orbs restrictions box."""
		self.orbrestrEdit.clear()
		all = all_orbs_restrictions_names()
		self.orbrestrEdit.addItems(all)
		i = all.index(self._filt._orbrestr._name)
		self.orbrestrEdit.setCurrentIndex(i)
	
	def reset(self):
		"""Reset entries."""
		filt = self._filt
		# name
		self.nameEdit.setText(filt._name)
		# planets
		self.resetPlanetsFilters()
		# aspects
		self.resetAspectsFilters()
		# orbs
		self.resetOrbsFilters()
		# aspects restrictions
		self.resetAspectsRestrictions()
		# orbs modifiers
		self.resetOrbsRestrictions()
		# comment
		self.commentEdit.setPlainText(filt._comment)
	
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
		# planets filter
		planets = PlanetsFilter(
			all_planets_filters_names()[self.planetsEdit.currentIndex()])
		# aspects filter
		aspects = AspectsFilter(
			all_aspects_filters_names()[self.aspectsEdit.currentIndex()])
		# orbs filter
		orbs = OrbsFilter(
			all_orbs_filters_names()[self.orbsEdit.currentIndex()])
		# aspects restrictions
		asprestr = AspectsRestrictions(
			all_aspects_restrictions_names()[self.asprestrEdit.currentIndex()])
		# orbs restrictions
		orbrestr = OrbsRestrictions(
			all_orbs_restrictions_names()[self.orbrestrEdit.currentIndex()])
		# comment
		cmt = unicode(self.commentEdit.toPlainText())
		# ### set filter ###
		self._filt.set(name=name, planets=planets, aspects=aspects, orbs=orbs,
			asprestr=asprestr, orbrestr=orbrestr, comment=cmt)
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
			app.midPointsFilterUpdatedEvent(self._filt._idx_)
		# done
		self.done(PyQt5.QtWidgets.QDialog.Accepted)



def main():
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	main = MidPointsFilterDialog()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# End.
