/** @odoo-module */
import { Component, useState, reactive, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { renderToString } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";
import {
    lazyLoading,
    initIsotope,
    matchHeight,
    initHiddenGal,
} from "./common_utlities.js";

export class PopularProperties extends Component {
    static template = "tk_website_rental_management.dynamic_popular_properties";
    static props = {};
    async setup() {
        this.orm = useService("orm");
        this.popular_listing = useState({}); // Set State
        await this.getPopularPropertyData();
    }
    async getPopularPropertyData() {
        let popularPropertyData = await rpc("/get-popular-property-data", {}); // Get data from backend
        this.popular_listing = popularPropertyData; // Set data in state

        let element = document.querySelectorAll("#popular-properties");

        element.forEach((ele, index) => {
            let injectedContentStr = renderToString(
                "tk_website_rental_management.dynamic_popular_properties",
                { popular_listing: popularPropertyData }
            ); // Rerencer Template

            const domParser = new DOMParser(); // Create new domparser
            const parsedHTML = domParser.parseFromString(
                injectedContentStr,
                "text/html"
            ).body; // Convert String into html formate

            document
                .querySelectorAll("#dynamic-popular-properties")
                ?.forEach((element) => {
                    element.classList.add("p-section");
                });
            document
                .querySelectorAll("#static-popular-properties")
                ?.forEach((element) => {
                    element.innerHTML = "";
                });
            ele.innerHTML = "";
            ele.append(...parsedHTML.children); // append that html into DOM

            setTimeout(() => {
                lazyLoading(); // Initialize lazy loading after rendering
            }, 1000);
            initIsotope(); // Initialization of Isotope for images and gallery items
            matchHeight(); // For cards align equal height
            initHiddenGal(this.popular_listing); // Initialization of Hidden Gallery
        });
    }
}

registry
    .category("public_components")
    .add(
        "tk_website_rental_management.dynamic_popular_properties",
        PopularProperties
    );
