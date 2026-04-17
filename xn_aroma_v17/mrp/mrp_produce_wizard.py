# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class XnAromaMRP(models.TransientModel):
	_inherit = 'mrp.product.produce'

	lot_id = fields.Many2one('stock.lot', string='Lot',readonly=True)

	def xn_update(self):
		for line in self.produce_line_ids:
			lot = line.lot_id and line.lot_id.name
		lot_obj = self.env['stock.lot'].search([('name','=',lot),('product_id','=',self.product_id.id)])
		if len(lot_obj) != 0:
			self.lot_id = lot_obj[0]
		else :
			values = {}
			for line in self.produce_line_ids:
				values['name'] = line.lot_id.name
				values['product_id'] = self.product_id and self.product_id.id
			lot_obj = self.env['stock.lot'].create(values)
			self.lot_id = lot_obj.id
		return {
			'context': self.env.context,
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'mrp.product.produce',
			'res_id': self.id,
			'view_id': False,
			'type': 'ir.actions.act_window',
			'target': 'new',
		}		

	def do_produce(self):
		res = super(XnAromaMRP, self).do_produce()
		for line in self.produce_line_ids:
			if line.qty_done <= 0:
				raise UserError(_('Done Quantity should be greater than 0'))
		return res


