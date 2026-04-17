# -*- coding: utf-8 -*-

import base64
import re

from odoo import _, api, fields, models, SUPERUSER_ID, tools
from odoo.tools import pycompat
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError

class XnMailComposer(models.TransientModel):
	_inherit = 'mail.compose.message'

	def render_message(self, res_ids):
		self.ensure_one()
		multi_mode = True
		if isinstance(res_ids, pycompat.integer_types):
			multi_mode = False
			res_ids = [res_ids]

		subjects = self.render_template(self.subject, self.model, res_ids)
		bodies = self.render_template(self.body, self.model, res_ids, post_process=True)
		emails_from = self.render_template(self.email_from, self.model, res_ids)
		replies_to = self.render_template(self.reply_to, self.model, res_ids)
		default_recipients = {}
		if not self.partner_ids:
			default_recipients = self.env['mail.thread'].message_get_default_recipients(res_model=self.model, res_ids=res_ids)

		notification_mail_id_param =self.env['ir.config_parameter'].sudo().search([('key','=','notification_mail_id_param')])
		if len(notification_mail_id_param) == 0 :
			raise UserError(_("Please set a parameter \'notification_mail_id_param\' for Notification Mail Id"))

		results = dict.fromkeys(res_ids, False)
		for res_id in res_ids:
			results[res_id] = {
				'subject': subjects[res_id],
				'body': bodies[res_id],
				# 'email_from': emails_from[res_id], #previous
				'email_from': notification_mail_id_param.value,
				'reply_to': replies_to[res_id],
			}
			results[res_id].update(default_recipients.get(res_id, dict()))

		# generate template-based values
		if self.template_id:
			template_values = self.generate_email_for_composer(
				self.template_id.id, res_ids,
				fields=['email_to', 'partner_to', 'email_cc', 'attachment_ids', 'mail_server_id'])
		else:
			template_values = {}

		for res_id in res_ids:
			if template_values.get(res_id):
				# recipients are managed by the template
				results[res_id].pop('partner_ids')
				results[res_id].pop('email_to')
				results[res_id].pop('email_cc')
				# remove attachments from template values as they should not be rendered
				template_values[res_id].pop('attachment_ids', None)
			else:
				template_values[res_id] = dict()
			# update template values by composer values
			template_values[res_id].update(results[res_id])

		return multi_mode and template_values or template_values[res_ids[0]]