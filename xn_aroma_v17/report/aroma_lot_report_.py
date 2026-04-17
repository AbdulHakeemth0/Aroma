from odoo import models, fields,api, _

class AromaInvoiceReport(models.Model):
	_inherit = "stock.lot"

	@api.model
	def render_html(self, docids, data=None):
		report_obj = self.env['report']
		report = report_obj._get_report_from_name('xn_aroma_v11.aroma_lot_report1')
		docargs = {
			'doc_ids': docids,
			'doc_model': report.sale_order,
			'docs': self,
		}
		return report_obj.render('xn_aroma_v11.aroma_lot_report1', docargs)