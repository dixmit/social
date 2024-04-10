# Copyright 2024 Dixmit
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json

from odoo.http import Controller, request, route


class GatewayController(Controller):
    @route(
        "/gateway/<string:usage>/<string:token>/update",
        type="http",
        auth="public",
        methods=["GET", "POST"],
        csrf=False,
    )
    def post_update(self, usage, token, *args, **kwargs):
        if request.httprequest.method == "GET":
            bot_data = request.env["mail.gateway"]._get_gateway(
                token, gateway_type=usage, state="pending"
            )
            if not bot_data:
                return request.make_response(
                    json.dumps({}),
                    [
                        ("Content-Type", "application/json"),
                    ],
                )
            return (
                request.env["mail.gateway.%s" % usage]
                .with_user(bot_data["webhook_user_id"])
                ._receive_get_update(bot_data, request, **kwargs)
            )
        bot_data = request.env["mail.gateway"]._get_gateway(
            token, gateway_type=usage, state="integrated"
        )
        if not bot_data:
            return request.make_response(
                json.dumps({}),
                [
                    ("Content-Type", "application/json"),
                ],
            )
        jsonrequest = json.loads(
            request.httprequest.get_data().decode(request.httprequest.charset)
        )
        dispatcher = (
            request.env["mail.gateway.%s" % usage]
            .with_user(bot_data["webhook_user_id"])
            .with_context(no_gateway_notification=True)
        )
        if not dispatcher._verify_update(bot_data, jsonrequest):
            return request.make_response(
                json.dumps({}),
                [
                    ("Content-Type", "application/json"),
                ],
            )
        gateway = dispatcher.env["mail.gateway"].browse(bot_data["id"])
        dispatcher._receive_update(gateway, jsonrequest)
        return request.make_response(
            json.dumps({}),
            [
                ("Content-Type", "application/json"),
            ],
        )