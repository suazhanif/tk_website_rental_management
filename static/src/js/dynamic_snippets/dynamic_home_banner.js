/** @odoo-module */
import { Component, useState, reactive, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { renderToString } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";
import { lazyLoading } from "./common_utlities.js";
import { loadJsFile } from "../plugin_loader.js";

let dynamicNiceSelectValue = 1;

export class HomeBanner extends Component {
    static template = "tk_website_rental_management.dynamic_home_banner";
    static props = {};
    async setup() {
        this.home_config = useState({
            activeTab: "inpt1",
            home_config: {},
        }); // Set State
        await loadJsFile(
            "/tk_website_rental_management/static/src/js/plugins.js"
        );
        await this.getHomeConfigData();
    }
    async getHomeConfigData() {
        let homeConfigData = await rpc("/get-home-config-data", {}); // Get data from backend
        this.home_config = homeConfigData; // Set data in state

        let element = document.querySelectorAll(".home-banner");
        element.forEach(async (ele) => {
            this.home_config.dynamicVal = dynamicNiceSelectValue;
            let injectedContentStr = renderToString(
                "tk_website_rental_management.dynamic_home_banner",
                { home_config: this.home_config }
            ); // Rerencer Template

            const domParser = new DOMParser(); // Create new domparser
            const { children } = domParser.parseFromString(
                injectedContentStr,
                "text/html"
            ).body; // Convert String into html formate

            document
                .querySelectorAll("#static-home-banner")
                ?.forEach((element) => {
                    element.remove();
                });
            document.querySelectorAll(".s_home_banner")?.forEach((element) => {
                element.style.height = "";
            });
            ele.innerHTML = "";
            ele.append(...children); // append that html into DOM

            this.changeBG(); // Change BG of home section

            lazyLoading();

            $(`.dynamic-chosen-select-${dynamicNiceSelectValue}`).niceSelect();

            this.onClickChangeTabs(); // Change nav-tabs

            this.playVideo(dynamicNiceSelectValue); // For Play background video on homepage

            this.toggalModal(dynamicNiceSelectValue); // Open and close advance modal in filter section

            this.modelFilters(dynamicNiceSelectValue); // change filter according to selection

            dynamicNiceSelectValue++;
        });

        this.pricingAndAreaSlider(); // Initialization of pricing and area sliders

        this.onchangeAmenityFilters(); // Add filters on homepage advance model
    }
    changeBG() {
        /**
         * Change Bcakground Images on Click Nav-Tabs
         */
        var a = $(".bg");
        a.each(function (a) {
            if ($(this).attr("data-bg"))
                $(this).css(
                    "background-image",
                    "url(" + $(this).data("bg") + ")"
                );
        });
        $(".change_bg a").on("click", function () {
            var bgt = $(this).data("bgtab");
            $(".bg_tabs").css("background-image", "url(" + bgt + ")");
        });
    }
    playVideo(youotubeWrapperId) {
        /**
         * Play Videos youtube video
         */
            var v = $(
                `.dynamic-background-youtube-wrapper-${youotubeWrapperId}`
            ).data("vid");
            var f = $(
                `.dynamic-background-youtube-wrapper-${youotubeWrapperId}`
            ).data("mv");
            $(
                `.dynamic-background-youtube-wrapper-${youotubeWrapperId}`
            ).YTPlayer({
                fitToBackground: true,
                videoId: v,
                mute: true,
                callback: function () {
                    var a = $(
                        `.dynamic-background-youtube-wrapper-${youotubeWrapperId}`
                    ).data("ytPlayer").player;
                },
            });

            var w = $(".background-vimeo").data("vim"),
                bvc = $(".background-vimeo"),
                bvmc = $(".media-container"),
                bvfc = $(".background-vimeo iframe "),
                vch = $(".video-container");
            bvc.append(
                '<iframe src="//player.vimeo.com/video/' +
                    w +
                    '?background=1"  frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen ></iframe>'
            );
            $(".video-holder").height(bvmc.height());
            if ($(window).width() > 1024) {
                if ($(".video-holder").length > 0)
                    if ((bvmc.height() / 9) * 16 > bvmc.width()) {
                        bvfc.height(bvmc.height()).width(
                            (bvmc.height() / 9) * 16
                        );
                        bvfc.css({
                            "margin-left":
                                (-1 * $("iframe").width()) / 2 + "px",
                            top: "-75px",
                            "margin-top": "0px",
                        });
                    } else {
                        bvfc.width($(window).width()).height(
                            ($(window).width() / 16) * 9
                        );
                        bvfc.css({
                            "margin-left":
                                (-1 * $("iframe").width()) / 2 + "px",
                            "margin-top":
                                (-1 * $("iframe").height()) / 2 + "px",
                            top: "50%",
                        });
                    }
            } else if ($(window).width() < 760) {
                $(".video-holder").height(bvmc.height());
                bvfc.height(bvmc.height());
            } else {
                $(".video-holder").height(bvmc.height());
                bvfc.height(bvmc.height());
            }
            vch.css("width", $(window).width() + "px");
            vch.css("height", (720 / 1280) * $(window).width()) + "px";

            if (vch.height() < $(window).height()) {
                vch.css("height", $(window).height() + "px");
                vch.css("width", (1280 / 720) * $(window).height()) + "px";
            }
    }
    onClickChangeTabs() {
        /**
         * On click change tab link and content
         */
        const tabs = document.querySelectorAll(".snippet-tab-li");
        tabs.forEach((tab) => {
            let tabId = tab.getAttribute("data-tab-id");
            tab.addEventListener("click", () => {
                const firstTab = document.getElementById(
                    `snippet-tab-inpt1-${tabId}`
                );
                const secondTab = document.getElementById(
                    `snippet-tab-inpt2-${tabId}`
                );
                const thirdTab = document.getElementById(
                    `snippet-tab-inpt3-${tabId}`
                );

                tabs.forEach((el) => {
                    if (el.getAttribute("data-tab-id") == tabId) {
                        el.classList.remove("current");
                    }
                });
                tab.classList.add("current");

                if (firstTab.classList.contains("first-tab")) {
                    firstTab.classList.remove("first-tab");
                }
                if (secondTab.classList.contains("first-tab")) {
                    secondTab.classList.remove("first-tab");
                }
                if (thirdTab.classList.contains("first-tab")) {
                    thirdTab.classList.remove("first-tab");
                }

                let currentElementId = tab.getAttribute("id");
                if (currentElementId == "snippet-tab-li1") {
                    firstTab.classList.add("first-tab");
                } else if (currentElementId == "snippet-tab-li2") {
                    secondTab.classList.add("first-tab");
                } else {
                    thirdTab.classList.add("first-tab");
                }

                $(".change_bg a").on("click", function () {
                    var bgt = $(this).data("bgtab");
                    $(".bg_tabs").css("background-image", "url(" + bgt + ")");
                });
            });
        });
    }
    toggalModal(dynamicVal) {
        /**
         * Toggal modal fron nav-tab content
         */
        var modal = {};
        modal.hide = function () {
            $(
                `.dynamic-modal-${dynamicVal} , .dynamic-reg-overlay-${dynamicVal}`
            ).fadeOut(200);
            $("html, body").removeClass("hid-body");
            $(`.dynamic-modal_main-${dynamicVal}`).removeClass("vis_mr");
        };
        $(`.dynamic-modal-open-${dynamicVal}`).on("click", function (e) {
            e.preventDefault();
            $(
                `.dynamic-modal-${dynamicVal} , .dynamic-reg-overlay-${dynamicVal}`
            ).fadeIn(200);
            $(`.dynamic-modal_main-${dynamicVal}`).addClass("vis_mr");
            $("html, body").addClass("hid-body");
        });
        $(
            `.dynamic-close-reg-${dynamicVal} , .dynamic-reg-overlay-${dynamicVal}`
        ).on("click", function () {
            modal.hide();
        });
    }
    modelFilters(dynamicVal) {
        /**
         * change filter according to selection
         */
        // Homepage Advance Filters
        $(".advance_any_filter_button").on("click", function () {
            $(".advance_st").val($(`.advance_any_status-${dynamicVal}`).val());
            $(".advance_search_term").val(
                $(`.advance_any_search_term-${dynamicVal}`).val()
            );
            $(".advance_max_prd").val(
                $(`.advance_any_max_prc-${dynamicVal}`).val()
            );
            $(".advance_cn").val($(`.advance_any_city-${dynamicVal}`).val());
        });

        $(".advance_rent_filter_button").on("click", function () {
            $(".advance_st").val($(`.advance_rent_status-${dynamicVal}`).val());
            $(".advance_search_term").val(
                $(`.advance_rent_search_term-${dynamicVal}`).val()
            );
            $(".advance_max_prd").val(
                $(`.advance_rent_max_prc-${dynamicVal}`).val()
            );
            $(".advance_cn").val($(`.advance_rent_city-${dynamicVal}`).val());
        });

        $(".advance_sale_filter_button").on("click", function () {
            $(".advance_st").val($(`.advance_sale_status-${dynamicVal}`).val());
            $(".advance_search_term").val(
                $(`.advance_sale_search_term-${dynamicVal}`).val()
            );
            $(".advance_max_prd").val(
                $(`.advance_sale_max_prc-${dynamicVal}`).val()
            );
            $(".advance_cn").val($(`.advance_sale_city-${dynamicVal}`).val());
        });

        $(`.advance_category-${dynamicVal}`).on("change", function () {
            let categoryValue = $(this).val();

            if (categoryValue === "residential") {
                $(`.advance_rooms-${dynamicVal}`).removeClass("d-none");
                $(`.advance_bathrooms-${dynamicVal}`).removeClass("d-none");
                $(`.advance_floors-${dynamicVal}`).removeClass("d-none");
            } else if (categoryValue === "commercial") {
                $(`.advance_rooms-${dynamicVal}`).addClass("d-none");
                $(`.advance_bathrooms-${dynamicVal}`).removeClass("d-none");
                $(`.advance_floors-${dynamicVal}`).removeClass("d-none");
            } else {
                $(`.advance_rooms-${dynamicVal}`).addClass("d-none");
                $(`.advance_bathrooms-${dynamicVal}`).addClass("d-none");
                $(`.advance_floors-${dynamicVal}`).addClass("d-none");
            }

            rpc("/property/advance-filters", {
                category_value: categoryValue,
            }).then(function (result) {
                let text =
                    '<option selected="selected">All Sub Categories</option>';
                if (result.categories_id.length > 0) {
                    $("#sub_category_div").removeClass("d-none");
                    result.categories_name.map((e, i) => {
                        text += `<option value="0${result.categories_id[i]}">${e}</option>`;
                    });

                    $(".advance_sub_category").empty().append(text);
                    $(".chosen-select").niceSelect("destroy"); //destroy the plugin
                    $(".chosen-select").niceSelect(); //apply again
                } else {
                    if (!$("#sub_category_div").hasClass("d-none")) {
                        $("#sub_category_div").addClass("d-none");
                    }
                }
            });
        });
    }
    pricingAndAreaSlider() {
        /**
         * Initialization of pricing and area sliders
         */
        $(".area-range").ionRangeSlider({
            type: "double",
            min: this.home_config.home_config.area_start,
            max: this.home_config.home_config.area_end,
        });
        $(".price-range").ionRangeSlider({
            type: "double",
            min: this.home_config.home_config.price_start,
            max: this.home_config.home_config.price_end,
        });
        function get_query() {
            var url = document.location.href;
            var qs = url.substring(url.indexOf("?") + 1).split("&");
            for (var i = 0, result = {}; i < qs.length; i++) {
                qs[i] = qs[i].split("=");
                result[qs[i][0]] = decodeURIComponent(qs[i][1]);
            }
            return result;
        }
        var result = get_query();
        if (
            result["price-start"] !== undefined &&
            result["price-end"] !== undefined
        ) {
            $(".price-range").data("ionRangeSlider").update({
                from: result["price-start"],
                to: result["price-end"],
            });
            $(".price-range").removeClass("d-none");
        }
        if (
            result["area-start"] !== undefined &&
            result["area-end"] !== undefined
        ) {
            $(".area-range")
                .data("ionRangeSlider")
                .update({ from: result["area-start"], to: result["area-end"] });
        }
    }
    onchangeAmenityFilters() {
        $(".check-gym").on("click", function () {
            add_amt_attribute("check-gym", this, "gym");
        });
        $(".check-wifi").on("click", function () {
            add_amt_attribute("check-wifi", this, "wifi");
        });
        $(".check-parking").on("click", function () {
            add_amt_attribute("check-parking", this, "parking");
        });
        $(".check-pool").on("click", function () {
            add_amt_attribute("check-pool", this, "pool");
        });
        $(".check-security").on("click", function () {
            add_amt_attribute("check-security", this, "security");
        });
        $(".check-laundry").on("click", function () {
            add_amt_attribute("check-laundry", this, "laundry");
        });
        $(".check-eq-kitchen").on("click", function () {
            add_amt_attribute("check-eq-kitchen", this, "kitchen");
        });
        $(".check-air-condition").on("click", function () {
            add_amt_attribute("check-air-condition", this, "ac");
        });
        $(".check-semi-furnish").on("click", function () {
            add_amt_attribute("check-semi-furnish", this, "smf");
        });
        $(".check-full-furnish").on("click", function () {
            add_amt_attribute("check-full-furnish", this, "fuf");
        });
        $(".check-alarm").on("click", function () {
            add_amt_attribute("check-alarm", this, "alarm");
        });
        $(".check-wc").on("click", function () {
            add_amt_attribute("check-wc", this, "wc");
        });
        $(".da").on("click", function () {
            let da = "";
            $(".da:checked").each(function () {
                da += $(this).data("id").toString() + ",";
            });
            $("#da").val(da);
        });
    }
}

function add_amt_attribute(id, self, name) {
    if (self.checked) {
        $(self).attr("name", "facility");
    } else {
        $(self).removeAttr("name");
    }
}

registry
    .category("public_components")
    .add("tk_website_rental_management.dynamic_home_banner", HomeBanner);
