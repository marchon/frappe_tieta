# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class StockSerialNo(Document):
	pass


def stock_serial_no_query(doctype, txt, searchfield, start, page_len, filters):
	if not filters:
		return frappe.db.sql("""select name, warehouse from `tabStock Serial No`
			where docstatus = 1
			and %s like %s order by name limit %s, %s""" %
			(searchfield, "%s", "%s", "%s"),
			("%%%s%%" % txt, start, page_len), as_list=1)

	item_code = filters["item_code"] or ''
	return frappe.db.sql("""select name, warehouse from `tabStock Serial No`
		where item_code = %s and docstatus = 1
		and %s like %s order by name limit %s, %s""" %
		("%s", searchfield, "%s", "%s", "%s"),
		(item_code, "%%%s%%" % txt, start, page_len), as_list=1)