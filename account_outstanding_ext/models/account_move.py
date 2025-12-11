import json
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('move_type', 'line_ids.amount_residual')
    def _compute_payments_widget_to_reconcile_info(self):
        #Ejecutamos el método original de Odoo
        super()._compute_payments_widget_to_reconcile_info()

        #Recorremos los resultados para inyectar tus datos extra
        for move in self:
            # Si no hay widget calculado (ej. factura pagada o borrador), saltamos
            if not move.invoice_outstanding_credits_debits_widget:
                continue

            try:
                #Convertimos el JSON de Odoo a Diccionario Python
                data = json.loads(move.invoice_outstanding_credits_debits_widget)
                modified = False

                if data and 'content' in data:
                    for line in data['content']:
                        if line.get('move_id'):
                            #Buscamos el asiento contable original (El anticipo/pago)
                            payment_move = self.env['account.move'].browse(line['move_id'])

                            #Nombre (ej. PAGO/2023/001)
                            line['move_name'] = payment_move.name
                            #Referencia completa
                            line['ref_full'] = payment_move.ref or ''

                            modified = True

                if modified:
                    move.invoice_outstanding_credits_debits_widget = json.dumps(data)

            except Exception as e:
                _logger.error(f"Error actualizando widget de pagos: {e}")