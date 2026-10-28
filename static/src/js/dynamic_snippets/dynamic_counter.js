/** @odoo-module */
import { Component, useState, reactive, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { renderToString } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";
import { loadJsFile } from "../plugin_loader.js";

export class Counter extends Component {
    static template = "tk_website_rental_management.dynamic_counter";
    static props = {};
    async setup() {
        this.home_config = useState({}); // Set State
        await loadJsFile(
            "/tk_website_rental_management/static/src/js/plugins.js"
        );
        await this.getCounterData();
    }
    async getCounterData() {
        let counterData = await rpc("/get-counter-data", {}); // Get data from backend
        this.counter = counterData; // Set data in state

        let element = document.querySelectorAll("#counter");
        element.forEach(async (ele) => {
            let injectedContentStr = renderToString(
                "tk_website_rental_management.dynamic_counter",
                { home_config: counterData }
            ); // Rerencer Template

            const domParser = new DOMParser(); // Create new domparser
            const { children } = domParser.parseFromString(
                injectedContentStr,
                "text/html"
            ).body; // Convert String into html formate

            document
                .querySelectorAll("#dynamic-counter")
                ?.forEach((element) => {
                    element.innerHTML = "";
                });
            ele.innerHTML = "";
            ele.append(...children); // append that html into DOM

            var a = $(".bg");
            a.each(function (a) {
                if ($(this).attr("data-bg"))
                    $(this).css(
                        "background-image",
                        "url(" + $(this).data("bg") + ")"
                    );
            });

            $(".dynamic-stats").appear(function () {
                $(".dynamic-num").countTo();
            });
        });
    }
}

registry
    .category("public_components")
    .add("tk_website_rental_management.dynamic_counter", Counter);
