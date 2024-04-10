/** @odoo-module **/

import {registerPatch} from "@mail/model/model_core";

registerPatch({
    name: "MessagingInitializer",
    recordMethods: {
        async _init({gateways}) {
            const discuss = this.messaging.discuss;
            this.messaging.executeGracefully(
                gateways.map((gatewayData) => () => {
                    this.messaging.models.DiscussSidebarCategory.insert({
                        discussAsGateways: discuss,
                        ...gatewayData,
                    });
                })
            );
            this._super(...arguments);
        },
    },
});
