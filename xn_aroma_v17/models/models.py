# -*- coding: utf-8 -*-

from odoo import models, fields, api

class xn_Insurance(models.Model):
	_name = 'xn_insurance_id'
	
	name = fields.Char(string = 'Insurance')
		
class xn_Packaging(models.Model):
	_name = 'xn_packaging'
	
	name = fields.Char(string = 'Packaging')

class xn_Transportation(models.Model):
	_name = 'xn_transportation_id'
	
	name = fields.Char(string = 'Transportation')