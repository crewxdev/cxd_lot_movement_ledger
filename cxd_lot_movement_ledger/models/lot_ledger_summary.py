from odoo import models, fields, tools

class LotLedgerSummary(models.Model):
    _name = "lot.ledger.summary"
    _description = "Lot Ledger Summary"
    _auto = False
    _rec_name = "lot_id"

    lot_id = fields.Many2one("stock.lot", readonly=True)
    product_id = fields.Many2one("product.product", readonly=True)

    actual_qty = fields.Float(string="Actual Qty", readonly=True)
    remaining_qty = fields.Float(string="Remaining Qty", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    MIN(lml.id) AS id,
                    lml.lot_id,
                    lml.product_id,

                    SUM(CASE WHEN lml.move_type = 'in' THEN lml.qty ELSE 0 END) AS actual_qty,

                    SUM(
                        CASE
                            WHEN lml.move_type = 'in' THEN lml.qty
                            WHEN lml.move_type = 'out' THEN -lml.qty
                            ELSE 0
                        END
                    ) AS remaining_qty

                FROM lot_movement_ledger lml
                GROUP BY lml.lot_id, lml.product_id
            )
        """)

    def action_view_moves(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Lot Movements",
            "res_model": "stock.move.line",
            "view_mode": "list,form",
            "domain": [
                ("lot_id", "=", self.lot_id.id),
                ("state", "=", "done"),
            ],
            "context": {
                "search_default_lot_id": self.lot_id.id,
            }
        }

