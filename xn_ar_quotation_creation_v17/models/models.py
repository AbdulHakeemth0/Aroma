from odoo import models, fields, api,_

class AromaProductcategory(models.Model):
	_inherit='product.category'

	xn_allow_place_order=fields.Boolean(string="Allow Place Order ",default=False )

class AromaProductTemplate(models.Model):
	_inherit='product.template'

	xn_price_usd = fields.Float(string="Rate (USD)", compute = '_xn_price_usd',store = True)

	@api.depends('list_price')
	def _xn_price_usd(self):
		price_usd_param_obj = self.env['ir.config_parameter'].search([('key','=','xn_pdt_usd_rate')])
		if price_usd_param_obj.value != 0:
			self.xn_price_usd = self.list_price / float(price_usd_param_obj.value)	

class AromaProductProduct(models.Model):
	_inherit='product.product'

	xn_quantity=fields.Integer(string="Quantity")
	xn_amount=fields.Float(string="Amount",compute = '_xn_amount')
	xn_allow_place_order=fields.Boolean(related='categ_id.xn_allow_place_order')
	xn_price_usd=fields.Float(string="Rate (USD)", compute = '_xn_price_usd',store = True,related = 'product_tmpl_id.xn_price_usd')

	@api.depends('lst_price')
	def _xn_price_usd(self):
		price_usd_param_obj = self.env['ir.config_parameter'].search([('key','=','xn_pdt_usd_rate')])
		if price_usd_param_obj.value != 0:
			self.xn_price_usd = self.lst_price / float(price_usd_param_obj.value)

	@api.depends('xn_price_usd','xn_quantity')
	def _xn_amount(self):
		self.xn_amount = self.xn_price_usd * self.xn_quantity
	

