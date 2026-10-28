/** @odoo-module */
import { Component, useState, reactive, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { renderToString } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";
import { loadJsFile } from "../plugin_loader.js";

export class Partners extends Component {
    static template = "tk_website_rental_management.dynamic_partners";
    static props = {};
    async setup() {
        this.partner_ids = useState({}); // Set State
        await this.getPopularPropertyData();
    }
    async getPopularPropertyData() {
        let partnerData = await rpc("/get-partners-data", {}); // Get data from backend
        this.partner_ids = partnerData; // Set data in state

        let element = document.querySelectorAll("#partners");
        element.forEach(async (ele) => {
            let injectedContentStr = renderToString(
                "tk_website_rental_management.dynamic_partners",
                { partner_ids: partnerData }
            ); // Rerencer Template

            const domParser = new DOMParser(); // Create new domparser
            const { children } = domParser.parseFromString(
                injectedContentStr,
                "text/html"
            ).body; // Convert String into html formate

            document
                .querySelectorAll("#static-partners")
                ?.forEach((element) => {
                    element.innerHTML = "";
                });
            document
                .querySelectorAll("#dynamic-partners")
                ?.forEach((element) => {
                    element.style.height = "";
                });
            ele.innerHTML = "";
            ele.append(...children); // append that html into DOM
            await this.initSwiper(); // Initialization of lazy loading
        });
    }
    async initSwiper() {
        $(document).ready(async function () {
            if ($(".dynamic-clients-carousel").length > 0) {
                await loadJsFile(
                    "/tk_website_rental_management/static/src/js/plugins.js"
                );
                var j2 = new Swiper(".dynamic-clients-carousel", {
                    preloadImages: false,
                    freeMode: false,
                    slidesPerView: 5,
                    spaceBetween: 10,
                    loop: true,
                    grabCursor: true,
                    mousewheel: false,
                    navigation: {
                        nextEl: ".cc-next",
                        prevEl: ".cc-prev",
                    },
                    breakpoints: {
                        1064: {
                            slidesPerView: 3,
                        },
                        768: {
                            slidesPerView: 2,
                        },
                        520: {
                            slidesPerView: 1,
                        },
                    },
                });
            }
        });
    }
}

registry
    .category("public_components")
    .add("tk_website_rental_management.dynamic_partners", Partners);
