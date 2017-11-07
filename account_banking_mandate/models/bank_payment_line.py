# Copyright 2014 Compassion CH - Cyril Sester <csester@compassion.ch>
# Copyright 2014 Serv. Tecnol. Avanzados - Pedro M. Baeza
# Copyright 2015-2016 Akretion - Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BankPaymentLine(models.Model):
    _inherit = 'bank.payment.line'

    mandate_id = fields.Many2one(
        comodel_name='account.banking.mandate', string='Direct Debit Mandate',
        related='payment_line_ids.mandate_id')

    @api.model
    def same_fields_payment_line_and_bank_payment_line(self):
        res = super(BankPaymentLine, self).\
            same_fields_payment_line_and_bank_payment_line()
        res.append('mandate_id')
        return res

    @api.constrains('mandate_id', 'company_id')
    def _check_company_constrains(self):
        for line in self:
            if line.mandate_id.company_id != line.company_id:
                raise ValidationError(_(
                    "The bank payment line %s has a different company than "
                    "that of the linked mandate %s).") %
                    (line.name, line.mandate_id.name))
