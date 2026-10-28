/** @odoo-module */
import { Component, useState, reactive, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { renderToString } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";
import { loadJsFile } from "../plugin_loader.js";

export class Testimonials extends Component {
    static template = "tk_website_rental_management.dynamic_testimonials";
    static props = {};
    async setup() {
        this.review_ids = useState({}); // Set State
        await this.getPopularPropertyData();
    }
    async getPopularPropertyData() {
        let testimonialsData = await rpc("/get-testimonials-data", {}); // Get data from backend
        this.review_ids = testimonialsData; // Set data in state

        let element = document.querySelectorAll("#testimonials-cards");
        element.forEach(async (ele) => {
            let injectedContentStr = renderToString(
                "tk_website_rental_management.dynamic_testimonials",
                { review_ids: testimonialsData }
            ); // Rerencer Template

            const domParser = new DOMParser(); // Create new domparser
            const { children } = domParser.parseFromString(
                injectedContentStr,
                "text/html"
            ).body; // Convert String into html formate

            document
                .querySelectorAll("#dynamic-testimonials")
                ?.forEach((element) => {
                    element.classList.add("p-section");
                    element.classList.remove("static-p-section");
                });
            document
                .querySelectorAll("#static-testimonials")
                ?.forEach((element) => {
                    element.innerHTML = "";
                });
            ele.innerHTML = "";
            ele.append(...children); // append that html into DOM
            await this.initSwiper(); // Initialization of lazy loading
        });
    }
    async initSwiper() {
        $(document).ready(async function () {
            if ($(".dynamic-testimonilas-carousel").length > 0) {
                await loadJsFile(
                    "/tk_website_rental_management/static/src/js/plugins.js"
                );
                var j2 = new Swiper(".dynamic-testimonilas-carousel", {
                    preloadImages: false,
                    slidesPerView: 3,
                    spaceBetween: 20,
                    loop: true,
                    grabCursor: true,
                    mousewheel: false,
                    centeredSlides: true,
                    pagination: {
                        el: ".tc-pagination",
                        clickable: true,
                        dynamicBullets: true,
                    },
                    navigation: {
                        nextEl: ".listing-carousel-button-next",
                        prevEl: ".listing-carousel-button-prev",
                    },
                    breakpoints: {
                        1064: {
                            slidesPerView: 2,
                        },
                        640: {
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
    .add("tk_website_rental_management.dynamic_testimonials", Testimonials);
