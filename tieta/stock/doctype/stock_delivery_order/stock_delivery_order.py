# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document
from frappe.desk.form import assign_to


class StockDeliveryOrder(Document):
	def validate(self):
		for item in self.items:
			item.uom = frappe.get_value("Stock Item", item.item_type, "stock_uom")
			item.item_name = frappe.get_value("Stock Item", item.item_type, "item_name")
			if not item.serial_no:
				continue
			item.batch_no = frappe.get_value("Stock Serial No", item.serial_no, "batch_no")
			doc = frappe.get_doc("Stock Serial No", item.serial_no)
			if not doc:
				throw(_("Serial NO is not validate! {0}").format(item.serial_no))
			if doc.warehouse != self.warehouse:
				throw(_("Serial NO {0} is not in Warehouse {1} but in {2}").format(
					item.serial_no, self.warehouse, doc.warehouse))

	def on_submit(self):
		if not self.warehouse:
			throw(_("Ware house is required!!"))
		if self.order_source_type == 'Tickets Ticket':
			doc = frappe.get_doc('Tickets Ticket', self.order_source_id)
			doc.run_method("on_delivery_order_commit", self)
			try:
				assign_to.add({
					'assign_to': self.owner,
					'doctype': self.doctype,
					'name': self.name,
					'description': _("Delivery Order approved!"),
					'date': self.planned_date,
					'priority': 'High',
					'notify': 0
				})
			except assign_to.DuplicateToDoError:
				frappe.message_log.pop()
				pass

		for item in self.items:
			if not item.serial_no:
				continue
			doc = frappe.get_doc("Stock Serial No", item.serial_no)
			if not doc:
				throw(_("Serial NO is not validate! {0}").format(item.serial_no))
			if doc.warehouse != self.warehouse:
				throw(_("Serial NO {0} is not in Warehouse {1} but in {2}").format(
					item.serial_no, self.warehouse, doc.warehouse))
			doc.warehouse = None
			doc.save()

	def on_cancel(self):
		if self.order_source_type == 'Tickets Ticket':
			doc = frappe.get_doc('Tickets Ticket', self.order_source_id)
			doc.run_method("on_delivery_order_cancel")

		for item in self.items:
			if not item.serial_no:
				continue
			doc = frappe.get_doc("Stock Serial No", item.serial_no)
			if not doc:
				throw(_("Serial NO is not validate! {0}").format(item.serial_no))
			if doc.warehouse is not None:
				throw(_("Serial NO {0} is in Warehouse {1}").format(
					item.serial_no, doc.warehouse))
			doc.warehouse = self.warehouse
			doc.save()