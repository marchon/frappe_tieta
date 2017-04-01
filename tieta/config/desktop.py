# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "TieTa",
			"color": "#808000",
			"icon": "fa fa-podcast",
			"type": "module",
			"label": _("TieTa")
		},
		{
			"module_name": "Stock",
			"color": "#808000",
			"icon": "octicon octicon-package",
			"type": "module",
			"label": _("Stock")
		}
	]
