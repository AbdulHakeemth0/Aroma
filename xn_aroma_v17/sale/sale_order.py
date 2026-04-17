from odoo import models, fields, api

class AromaSaleOrder(models.Model):
	_inherit='sale.order'

	xn_insurance_id = fields.Many2one('xn_insurance_id',string = 'Insurance')
	xn_reference_no = fields.Char(string="Reference no")
	xn_description_of_goods = fields.Text(string = "Description Of Goods")
	xn_transportation_id =fields.Many2one('xn_transportation_id',string="Transportation")
	xn_delivery_status = fields.Selection([('waiting', 'Waiting'),('delivered', 'Delivered'),('canceled','Canceled')], string="Delivery Status",compute = '_compute_xn_delivery_status',store = True)
	xn_contact_id = fields.Many2one('res.partner',string = "Contact",domain="[('parent_id', '=', partner_id),('type','=','contact')]")

	@api.depends('picking_ids','picking_ids.state')
	def _compute_xn_delivery_status(self):
		for record in self:
			flag = 0
			done_count = 0
			waiting_count = 0
			canceled_count = 0
			total_count = len(record.picking_ids)
			if len(record.picking_ids) == 0:
				flag = 0
			else:
				flag = 1
			for picking in record.picking_ids:
				if picking.state == 'done':
					done_count = done_count + 1
				elif picking.state == 'cancel':
					canceled_count = canceled_count + 1
			if flag == 0:
				record.xn_delivery_status = False
			else:
				if done_count == total_count:
					record.xn_delivery_status = 'delivered'
				elif canceled_count == total_count:
					record.xn_delivery_status = 'canceled'
				else:
					record.xn_delivery_status = 'waiting'

	def _prepare_invoice(self):
		res = super(AromaSaleOrder, self)._prepare_invoice()
		res['xn_reference_no'] = self.xn_reference_no
		res['xn_insurance_id'] = self.xn_insurance_id and self.xn_insurance_id.id
		res['xn_description_of_goods'] = self.xn_description_of_goods
		res['xn_transportation_id'] = self.xn_transportation_id and self.xn_transportation_id.id
		res['xn_contact_id'] = self.xn_contact_id and self.xn_contact_id.id or False
		return res