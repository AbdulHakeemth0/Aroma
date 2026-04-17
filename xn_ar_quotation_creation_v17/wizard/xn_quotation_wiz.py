# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api,_
from odoo.exceptions import UserError


class QuotationCreation(models.TransientModel):
	_name = "xn_quotation_creation_wiz"

	xn_customer_id = fields.Many2one('res.partner',string = "Customer",domain=[('customer', '=', True),('parent_id', '=', False)])
	xn_payment_term_id = fields.Many2one('account.payment.term', string="Payment Terms",readonly = True)
	xn_date=fields.Datetime(string="Date",default=lambda self: fields.datetime.now())
	xn_quotation_type = fields.Selection([('new', 'New Order'),('merge', 'Merge With Existing Quotation')], string="Quotation",default = "new")
	xn_quotation_id = fields.Many2one('sale.order', string="Select Quotation")
	xn_shipping_mode_id = fields.Many2one('xn_transportation_id',string = "Shipping Mode")
	xn_shipping_address_id = fields.Many2one('res.partner',string = "Shipping Adress",compute='_compute_shipping_address',store=True)
	xn_quotation_lines = fields.One2many('xn_quotation_creation_line','xn_quotation_line_id')
	xn_note = fields.Text()
	
	@api.model
	def default_get(self,default_fields):
		res = super(QuotationCreation, self).default_get(default_fields)
		user_obj = self.env['res.users'].browse(self._uid)
		product_id = self._context.get('active_ids')	
		product_obj = self.env['product.product'].browse(product_id)
		product_wiz_lines = []
		for products in product_obj:
			product_wiz_lines.append([0,0,{'xn_product_id':products.id,
				'xn_qty' : products.xn_quantity,
				'xn_rate':products.xn_price_usd,
				'xn_amount_wiz':products.xn_amount 
				}])
			products.xn_quantity = 0
		res.update({'xn_quotation_lines':product_wiz_lines})
		res.update({'xn_customer_id':user_obj.partner_id and user_obj.partner_id.id})
		res.update({'xn_payment_term_id':user_obj.partner_id.property_payment_term_id and user_obj.partner_id.property_payment_term_id.id or False})
		return res

	@api.depends('xn_customer_id')
	def _compute_shipping_address(self):
		for child in self.xn_customer_id.child_ids :
			if child.type == 'delivery' :
				self.xn_shipping_address_id = child.id

	def xn_mergequotation(self):
		if self.xn_quotation_type == "merge":
			if self.xn_quotation_id.state != 'draft' :
				raise UserError(_('Quotation must be in draft state'))
			order_lines = []

			for line in self.xn_quotation_lines:
				order_line_data = (0,0,{
										'product_id':line.xn_product_id and line.xn_product_id.id,
										'name':line.xn_product_id.name,
										'product_uom_qty':line.xn_qty,
										'product_uom':line.xn_product_id.uom_id and line.xn_product_id.uom_id.id
										})
				order_lines.append(order_line_data)
			self.xn_quotation_id.update({'order_line':order_lines})	
			return {
               'name': "Quotation",
               'type': 'ir.actions.act_window',
               'view_mode': 'tree,form',
                'tree_view_id': self.env.ref('sale.view_quotation_tree').id,               
                'form_view_id': self.env.ref('sale.view_order_form').id,               
               'target': 'current',
               'res_model':'sale.order',
               'domain': [('id','in',[self.xn_quotation_id.id])],
           }		

	def xn_create_quotation(self):
		if self.xn_quotation_type == "new":
			seq_parameter_obj = self.env['ir.config_parameter'].search([('key','=','xn_place_order_seq_key')])
			seq_obj = self.env['ir.sequence'].search([('id','=',seq_parameter_obj.value)])
			sales_channel_parameter_obj = self.env['ir.config_parameter'].search([('key','=','xn_order_sales_channel')])
			sales_channel_obj = self.env['crm.team'].search([('id','=',sales_channel_parameter_obj.value)])
			usd_pricelist_obj = self.env['ir.config_parameter'].search([('key','=','xn_sales_usd_pricelist')])

			if len(seq_obj) == 0:
				raise UserError(_('Please Define a Sequence and a System Parameter: \'xn_place_order_seq_key\' for Place Order'))

			if len(sales_channel_obj) == 0:
				raise UserError(_('Please Define System Parameter: \'xn_order_sales_channel\' for Sales Channel'))

			if len(usd_pricelist_obj) == 0:
				raise UserError(_('Please Define System Parameter: \'xn_sales_usd_pricelist\' for USD Pricelist'))


			values = {}
			values['name'] = self.env['ir.sequence'].next_by_code(seq_obj.code)
			values['partner_id'] = self.xn_customer_id and self.xn_customer_id.id
			values['date_order'] = self.xn_date
			values['payment_term_id'] = self.xn_payment_term_id and self.xn_payment_term_id.id
			values['team_id'] = sales_channel_obj.id
			values['user_id'] = self.xn_customer_id.user_id and self.xn_customer_id.user_id.id
			values['partner_shipping_id'] = self.xn_shipping_address_id and self.xn_shipping_address_id.id
			values['xn_transportation_id'] = self.xn_shipping_mode_id and self.xn_shipping_mode_id.id
			values['note']  = self.xn_note
			values['pricelist_id'] = usd_pricelist_obj.value

			quotation_obj = self.env['sale.order'].create(values)
			order_lines = []

			for line in self.xn_quotation_lines:
				if line.xn_qty == 0 :
					raise UserError(_('Quantity of the product "%s" can\'t be zero') %(line.xn_product_id.name))
				order_line_data = (0,0,{
										'product_id':line.xn_product_id and line.xn_product_id.id,
										'name':line.xn_product_id.name,
										'product_uom_qty':line.xn_qty,
										'product_uom':line.xn_product_id.uom_id and line.xn_product_id.uom_id.id,
										'price_unit':line.xn_product_id.xn_price_usd
										})
				order_lines.append(order_line_data)
			quotation_obj.update({'order_line':order_lines})
			return {
               'name': "Quotation",
               'type': 'ir.actions.act_window',
               'view_mode': 'tree,form',
                'tree_view_id': self.env.ref('sale.view_quotation_tree').id,               
                'form_view_id': self.env.ref('sale.view_order_form').id,               
               'target': 'current',
               'res_model':'sale.order',
               'domain': [('id','in',[quotation_obj.id])],
           }


class QuotationCreationLine(models.TransientModel):
	_name = "xn_quotation_creation_line"		

	xn_product_id = fields.Many2one('product.product',string='Product')
	xn_qty = fields.Integer(string='Quantity')
	xn_quotation_line_id = fields.Many2one('xn_quotation_creation_wiz')
	xn_rate = fields.Float(string="Rate")
	xn_amount_wiz=fields.Float(string="Amount")

	@api.onchange('xn_qty')
	def calc_amount(self):
		self.xn_amount_wiz = self.xn_qty * self.xn_rate

	@api.onchange('xn_product_id')
	def change_product(self):
		self.xn_rate = self.xn_product_id.xn_price_usd
		self.xn_amount_wiz = self.xn_qty * self.xn_rate
