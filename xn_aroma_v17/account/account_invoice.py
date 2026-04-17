from odoo import models, fields, api

class AromaAccountInvoice(models.Model):
	_inherit='account.move'

	xn_insurance_id = fields.Many2one('xn_insurance_id',string = 'Insurance')
	xn_reference_no=fields.Char(string="Reference no")
	xn_description_of_goods = fields.Text(string = "Description Of Goods")
	xn_transportation_id=fields.Many2one('xn_transportation_id',string="Transportation")
	xn_contact_id = fields.Many2one('res.partner',string = "Contact",domain="[('parent_id', '=', partner_id),('type','=','contact')]")
		
class AromaAccountInvoiceLines(models.Model):
	_inherit='account.move.line'

	xn_package_id = fields.Many2one('xn_packaging',string = 'Packaging')	
