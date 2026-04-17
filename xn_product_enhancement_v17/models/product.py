from odoo import models,fields,api,_

class Group(models.Model):
     _name='xn_group'

     name=fields.Char(string='Group')

class SubGroup(models.Model):
     _name='xn_sub_group'

     name=fields.Char(string='Sub Group')

class Type(models.Model):
     _name='xn_type'

     name=fields.Char(string='Type')

class SubType(models.Model):
     _name='xn_sub_type'

     name=fields.Char(string='Sub Type')

class Brand(models.Model):
     _name='xn_brand'

     name=fields.Char(string='Brand')

class ProductEnhancement(models.Model):
     _inherit='product.template'

     xn_group=fields.Many2one('xn_group',string='Group',help='Group')
     xn_sub_group=fields.Many2one('xn_sub_group',string='Sub Group',help='')
     xn_type=fields.Many2one('xn_type',string='Type',help='Type')
     xn_sub_type=fields.Many2one('xn_sub_type',string='Sub Type',help='Sub Type')
     xn_brand=fields.Many2one('xn_brand',string='Brand',help='Brand')
     xn_country=fields.Many2one('res.country',string='Country Of Origin',help='Country')



   

     

