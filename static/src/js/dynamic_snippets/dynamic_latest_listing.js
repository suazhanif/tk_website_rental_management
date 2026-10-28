/** @odoo-module */
import { Component, useState, reactive, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { renderToString } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";
import { lazyLoading } from "./common_utlities.js";
import { loadJsFile } from "../plugin_loader.js";

export class LatestListing extends Component {
    static template = "tk_website_rental_management.dynamic_latest_listing";
    static props = {};
    async setup() {
        this.orm = useService("orm");
        this.latest_listing = useState({}); // Set State
        await this.getLatestListingData();
    }
    async getLatestListingData() {
        let latestListingData = await rpc("/get-latest-listing-data", {}); // Get data from backend
        this.latest_listing = latestListingData; // Store in state

        let elements = document.querySelectorAll("#latest-listing");

        elements.forEach(async (ele) => {
            let injectedContentStr = renderToString(
                "tk_website_rental_management.dynamic_latest_listing",
                { latest_listing: latestListingData }
            ); // Rerencer Template

            const domParser = new DOMParser(); // Create new domparser
            const parsedHTML = domParser.parseFromString(
                injectedContentStr,
                "text/html"
            ).body; // Convert String into html formate

            document
                .querySelectorAll(".dynamic-latest-listing")
                ?.forEach((element) => {
                    element.classList.remove("static-p-section");
                    element.classList.add("p-section");
                });
            document
                .querySelectorAll("#static-latest-listing")
                ?.forEach((element) => {
                    element.innerHTML = "";
                });
            ele.innerHTML = "";
            ele.append(...parsedHTML.children); // append that html into DOM

            await this.initSlider(); // Initialize slider for this instance
            setTimeout(() => {
                lazyLoading(); // Initialize lazy loading after rendering
            }, 1000);
        });
    }

    async initSlider() {
        $(document).ready(async function () {
            if ($(".listing-slider").length > 0) {
                await loadJsFile(
                    "/tk_website_rental_management/static/src/js/plugins.js"
                );
                var lsw = new Swiper(".dynamic-listing-slider", {
                    preloadImages: false,
                    slidesPerView: 4,
                    spaceBetween: 15,
                    loop: true,

                    grabCursor: true,
                    mousewheel: false,
                    centeredSlides: true,
                    pagination: {
                        el: ".dynamic-tc-pagination2",
                        clickable: true,
                        dynamicBullets: true,
                    },
                    navigation: {
                        nextEl: ".dynamic-listing-carousel-button-next2",
                        prevEl: ".dynamic-listing-carousel-button-prev2",
                    },
                    breakpoints: {
                        1650: {
                            slidesPerView: 3,
                        },
                        1270: {
                            slidesPerView: 2,
                        },
                        850: {
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
    .add("tk_website_rental_management.dynamic_latest_listing", LatestListing);
