from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
class Aromavarientcreation(models.Model):
	_inherit = 'product.template'

	xn_varient_line = fields.One2many('xn_aroma_varient_uom_line','xn_varient_id')
	xn_aroma_variant_count = fields.Integer(string="Aroma variant count", default=0)
	xn_description = fields.Char(string="Description")
	xn_parent_id = fields.Many2one('product.template', string="Parent Product")
	is_visible_to_distributor = fields.Boolean(string="Is Visible to Distributor")

	def aroma_copy(self):
		self.xn_description = self.name
	
	def aroma_variant_creation(self):
		if not (self.barcode and self.default_code):
			raise ValidationError(_('Please Enter Internal Reference and Barcode in General Information'))
		if not self.xn_description:
			raise ValidationError(_('Please Enter Description(Product Name)'))
		if len(self.xn_varient_line) == 0 :
			raise ValidationError(_('Please Enter New Packages'))

		route_id = self.env["stock.location.route"].search([('name','=',"Manufacture")])

		for variants in self.xn_varient_line:
			product_obj = self.env['product.template']
			product_name = str(self.xn_description) + '-' + str(variants.xn_uom_id.name)
			if not variants.xn_status:
				self.xn_aroma_variant_count = self.xn_aroma_variant_count + 1
				vals = {'name':product_name,
						'type':self.type,
						'categ_id':self.categ_id and self.categ_id.id,
						'uom_id' :variants.xn_uom_id and variants.xn_uom_id.id,
						'uom_po_id' : variants.xn_uom_id and variants.xn_uom_id.id,
						'default_code':str(self.default_code) + '-' + str(self.xn_aroma_variant_count),
						'barcode':str(self.barcode) + '-' +	str(self.xn_aroma_variant_count),
						'list_price':variants.xn_list_price,
						'purchase_ok' : False ,
						'tracking' : self.tracking,
						'route_ids': [(6,0,[route_id.id])],
						'xn_parent_id' : self.id
						}
				product_created = product_obj.create(vals)
				variants.write({'xn_status':True})
				variants.write({'xn_product_id': product_created.id})

class Aromavarientcreations(models.Model):
	_name='xn_aroma_varient_uom_line'

	xn_varient_id = fields.Many2one('product.template')
	xn_uom_id = fields.Many2one('product.uom',string="Package")
	xn_list_price = fields.Float(string = "Selling Price")
	xn_status=fields.Boolean(string="flag" ,default=False)
	xn_product_id = fields.Many2one('product.template',string = "Parent Product",readonly = True)
