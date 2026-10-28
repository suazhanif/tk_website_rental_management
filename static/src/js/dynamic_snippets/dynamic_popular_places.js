/** @odoo-module */
import { Component, useState, reactive, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { renderToString } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";

export class PopularPlaces extends Component {
    static template = "tk_website_rental_management.dynamic_popular_places";
    static props = {};
    async setup() {
        this.city_ids = useState({}); // Set State
        await this.getPopularPropertyData();
    }
    async getPopularPropertyData() {
        let popularPlacesData = await rpc("/get-popular-places-data", {}); // Get data from backend
        this.city_ids = popularPlacesData; // Set data in state

        let element = document.querySelectorAll("#popular_places_component");
        element.forEach(async (ele) => {
            let injectedContentStr = renderToString(
                "tk_website_rental_management.dynamic_popular_places",
                { city_ids: popularPlacesData }
            ); // Rerencer Template

            const domParser = new DOMParser(); // Create new domparser
            const { children } = domParser.parseFromString(
                injectedContentStr,
                "text/html"
            ).body; // Convert String into html formate

            document
                .querySelectorAll("#dynamic-popular-places")
                ?.forEach((element) => {
                    element.classList.remove("static-p-section");
                    element.classList.add("p-section");
                });
            document.querySelectorAll("#static-places")?.forEach((element) => {
                element.innerHTML = "";
            });
            ele.innerHTML = "";
            ele.append(...children); // append that html into DOM
        });
        var a = $(".bg");
        a.each(function (a) {
            if ($(this).attr("data-bg"))
                $(this).css(
                    "background-image",
                    "url(" + $(this).data("bg") + ")"
                );
        });
    }
}

registry
    .category("public_components")
    .add("tk_website_rental_management.dynamic_popular_places", PopularPlaces);
