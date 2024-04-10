# Copyright 2024 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    """Update of res.partner class to take into account the gateway."""

    _inherit = "res.partner"

    gateway_channel_ids = fields.One2many(
        "res.partner.gateway.channel", inverse_name="partner_id"
    )

    def _get_channels_as_member(self):
        channels = super()._get_channels_as_member()
        if self.env.user.has_group("mail_gateway.gateway_user"):
            channels |= self.env["mail.channel"].search(
                [
                    ("channel_type", "=", "gateway"),
                    (
                        "channel_member_ids",
                        "in",
                        self.env["mail.channel.member"]
                        .sudo()
                        ._search(
                            [
                                ("partner_id", "=", self.id),
                                ("is_pinned", "=", True),
                            ]
                        ),
                    ),
                ]
            )
        return channels


class ResPartnerGatewayChannel(models.Model):
    _name = "res.partner.gateway.channel"
    _description = "Technical data used to get the gateway author"

    name = fields.Char(
        compute="_compute_name", store=True, readonly=False, required=True
    )
    partner_id = fields.Many2one("res.partner", required=True, readonly=True)
    gateway_id = fields.Many2one("mail.gateway", readonly=True)
    gateway_token = fields.Char(readonly=True)

    @api.depends("gateway_id")
    def _compute_name(self):
        for record in self:
            record.name = record.gateway_id.name
