import logging
import json
from odoo import models, api

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('move_type', 'line_ids.amount_residual')
    def _compute_payments_widget_to_reconcile_info(self):
        # Ejecutar el original
        super()._compute_payments_widget_to_reconcile_info()

        field_widget = self._fields['invoice_outstanding_credits_debits_widget']

        for move in self:
            try:
                # Leemos directo de la cache para NO disparar calculos de neuvo
                # (al recalcular, la salida no entrega nada y da False)
                if not self.env.cache.contains(move, field_widget):
                    continue

                widget_content = self.env.cache.get(move, field_widget)

                # Si el cache esta vacio, entocnes no hay info que mostrar
                if not widget_content:
                    continue

                data = None
                is_json_string = False

                if isinstance(widget_content, str):
                    data = json.loads(widget_content)
                    is_json_string = True
                elif isinstance(widget_content, dict):
                    data = widget_content

                # insrtar data
                changed = False
                if data and 'content' in data:
                    for line in data['content']:
                        if line.get('move_id'):
                            payment_move = self.env['account.move'].browse(line['move_id'])

                            line['move_name_custom'] = str(payment_move.name or '')
                            line['ref_custom'] = str(payment_move.ref or '')

                            changed = True

                # Guardar
                if changed:
                    new_value = json.dumps(data) if is_json_string else data
                    move.invoice_outstanding_credits_debits_widget = new_value

            except Exception as e:
                _logger.error(f">>> [ERROR account_payment_outstanding model] Falló la inyección en {move.name}: {e}")