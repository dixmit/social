/** @odoo-module **/

import {attr, one} from "@mail/model/model_field";
import {registerPatch} from "@mail/model/model_core";

registerPatch({
    name: "Message",
    fields: {
        gateway_type: attr(),
        gateway_channel_data: attr(),
        gatewayThread: one("Thread", {inverse: "messagesAsGatewayThread"}),
    },
    modelMethods: {
        convertData(data) {
            const data2 = this._super(data);
            data2.gateway_type = data.gateway_type;
            data2.gateway_channel_data = data.gateway_channel_data;
            if (
                data.gateway_thread_data &&
                Object.keys(data.gateway_thread_data).length > 0
            ) {
                data2.gatewayThread = data.gateway_thread_data;
            }
            return data2;
        },
    },
});
