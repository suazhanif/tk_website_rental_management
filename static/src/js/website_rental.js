/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";

$(".geodir-js-favorite_btn, .js_add_wishlist").on("click", function (e) {
    const tgClass = $(this).hasClass("liked");
    const access = $(this).data("access");
    const clearWishlist = $(this).find('.clear-wishlist')
    e.preventDefault();
    rpc("/property/wishlist", {
        toggle: tgClass,
        access: access,
    }).then(function (result) {
        if (tgClass) {
            $('.clear-wishlist').each(function() {
                if ($(this).data('access') == access) {
                    $(this).trigger('click');
                }
            })
        } else {
            if (result.property_data) {
                let propertyData = result.property_data
                let text = ""
                let dataText = ""
                dataText += `
                    <li>
                        <div class="widget-posts-img">
                            <a href="${propertyData.redirect_url}"><img src="${propertyData.image}" alt="${propertyData.name}" loading="lazy" /></a>
                        </div>
                        <div class="widget-posts-descr">
                            <h4><a href="${propertyData.redirect_url}">${propertyData.name}</a></h4>
                `
                if (propertyData.address) {
                    dataText += `
                            <div class="geodir-category-location fl-wrap"><a href="${propertyData.map_url}" target="_blank"><i class="fas fa-map-marker-alt"></i> ${propertyData.address}</a></div>
                    `
                }
                dataText += `
                            <div class="clear-wishlist" data-access="${propertyData.access_token}">
                                <i class="fal fa-times-circle"></i>
                            </div>
                        </div>
                    </li>
                `
                if ($('.book_prop_ul').length > 0) {
                    $('.no_book_prop').empty()
                    $('.book_prop_ul').append(dataText)
                } else {
                    text += `<ul class="no-list-style book_prop_ul">${dataText}</ul>`
                    $('.no_book_prop').empty()
                    $('.book_prop_section').empty().append(text)
                }
            }
        }
        if (result.count) {
            $(".cart-counter").text(result.count);
        } else {
            $(".cart-counter").text(0);
        }
    });
    $(this).toggleClass("liked");
});
$(document).on("click", ".clear-wishlist", function (c) {
    const access = $(this).data("access");
    rpc("/property/wishlist/clear", {
        access: access,
    }).then(function (result) {
        if (result.count) {
            if (result.count == 0) {
                $('.book_prop_section').append(`
                    <div class="no_book_prop">
                        <h6>You don't have any favourite property!</h6>
                    </div>
                `)
            }
            $(".cart-counter").text(result.count);
        } else {
            $('.book_prop_section').append(`
                <div class="no_book_prop">
                    <h6>You don't have any favourite property!</h6>
                </div>
            `)
            $(".cart-counter").text(0);
        }
    });
    $(this)
        .parent()
        .parent()
        .fadeOut("slow", function (c) {});
});
$("#sort_type").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("property_type=") >= 0) {
            window.location.href = current_url.replace(
                /\bproperty_type=[0-9a-zA-Z_@.#+-]{1,50}\b/,
                "property_type=" + this.value
            );
        } else {
            window.location.href = current_url + "&property_type=" + this.value;
        }
    } else {
        window.location.href = current_url + "?property_type=" + this.value;
    }
});
$("#price_type").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("price_order=") >= 0) {
            window.location.href = current_url.replace(
                /\bprice_order=[0-9a-zA-Z_@.#+-]{1,50}\b/,
                "price_order=" + this.value
            );
        } else {
            window.location.href = current_url + "&price_order=" + this.value;
        }
    } else {
        window.location.href = current_url + "?price_order=" + this.value;
    }
});

$(".price-range").on("change", function () {
    let slider = $(".price-range").data("ionRangeSlider");
    $("#price_start").attr("name", "price-start").val(slider.result.from);
    $("#price_end").attr("name", "price-end").val(slider.result.to);
});
$(".area-range").on("change", function () {
    let slider = $(".area-range").data("ionRangeSlider");
    $("#area_start").attr("name", "area-start").val(slider.result.from);
    $("#area_end").attr("name", "area-end").val(slider.result.to);
});

$("#check-gym").on("click", function () {
    add_amt_attribute("check-gym", this, "gym");
});
$("#check-wifi").on("click", function () {
    add_amt_attribute("check-wifi", this, "wifi");
});
$("#check-parking").on("click", function () {
    add_amt_attribute("check-parking", this, "parking");
});
$("#check-pool").on("click", function () {
    add_amt_attribute("check-pool", this, "pool");
});
$("#check-security").on("click", function () {
    add_amt_attribute("check-security", this, "security");
});
$("#check-laundry").on("click", function () {
    add_amt_attribute("check-laundry", this, "laundry");
});
$("#check-eq-kitchen").on("click", function () {
    add_amt_attribute("check-eq-kitchen", this, "kitchen");
});
$("#check-air-condition").on("click", function () {
    add_amt_attribute("check-air-condition", this, "ac");
});
$("#check-semi-furnish").on("click", function () {
    add_amt_attribute("check-semi-furnish", this, "smf");
});
$("#check-full-furnish").on("click", function () {
    add_amt_attribute("check-full-furnish", this, "fuf");
});
$("#check-alarm").on("click", function () {
    add_amt_attribute("check-alarm", this, "alarm");
});
$("#check-wc").on("click", function () {
    add_amt_attribute("check-wc", this, "wc");
});
$(".da").on("click", function () {
    let da = "";
    $(".da:checked").each(function () {
        da += $(this).data("id").toString() + ",";
    });
    $("#da").val(da);
});

// FILTERS
// STATUS FILTER
$(".status_filter").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("st=") >= 0) {
            window.location.href = current_url.replace(
                /\bst=[0-9a-zA-Z_@.#+-]{1,50}\b/,
                "st=" + this.value.replace(/\s/g, "")
            );
        } else {
            window.location.href =
                current_url + "&st=" + this.value.replace(/\s/g, "");
        }
    } else {
        window.location.href =
            current_url + "?st=" + this.value.replace(/\s/g, "");
    }
});

// CITY FILTER
$(".city_filter").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    let value = this.value.replace(" ", "+");

    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("cn=") >= 0) {
            window.location.href = current_url.replace(
                /\bcn=[0-9a-zA-Z_@.#+-]{1,50}\b/,
                "cn=" + value
            );
        } else {
            window.location.href = current_url + "&cn=" + value;
        }
    } else {
        window.location.href = current_url + "?cn=" + value;
    }
});

// CATEGORY FILTER
$(".category_filter").on("change", function () {
    let selectedCateg = this.value.replace(/\s/g, "");
    let url = new URL(window.location);
    let params = url.searchParams;

    params.set("categ", selectedCateg);
    if (selectedCateg == "lands" || selectedCateg == "industrial") {
        params.delete("rooms");
        params.delete("bathrooms");
        params.delete("floor");
    }

    let updatedUrl = url.pathname + "?" + params.toString();
    window.location.href = updatedUrl;
});

// SUB CATEGORY FILTER
$(".sub_category_filter").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("dc=") >= 0) {
            window.location.href = current_url.replace(
                /\bdc=[0-9a-zA-Z_@.#+-]{1,50}\b/,
                "dc=" + this.value.replace(/\s/g, "")
            );
        } else {
            window.location.href =
                current_url + "&dc=" + this.value.replace(/\s/g, "");
        }
    } else {
        window.location.href =
            current_url + "?dc=" + this.value.replace(/\s/g, "");
    }
});

// BEDROOMS FILTER
$(".bedrooms_filter").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("rooms=") >= 0) {
            window.location.href = current_url.replace(
                /\brooms=[0-9a-zA-Z_@.#+-]{1,50}\b/,
                "rooms=" + this.value
            );
        } else {
            window.location.href = current_url + "&rooms=" + this.value;
        }
    } else {
        window.location.href = current_url + "?rooms=" + this.value;
    }
});

// BATHROOMS FILTER
$(".bathrooms_filter").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("bathrooms=") >= 0) {
            window.location.href = current_url.replace(
                /\bbathrooms=[0-9a-zA-Z_@.#+-]{1,50}\b/,
                "bathrooms=" + this.value
            );
        } else {
            window.location.href = current_url + "&bathrooms=" + this.value;
        }
    } else {
        window.location.href = current_url + "?bathrooms=" + this.value;
    }
});

// FLOORS FILTER
$(".floor_filter").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("floor=") >= 0) {
            window.location.href = current_url.replace(
                /\bfloor=[0-9a-zA-Z_@.#+-]{1,50}\b/,
                "floor=" + this.value
            );
        } else {
            window.location.href = current_url + "&floor=" + this.value;
        }
    } else {
        window.location.href = current_url + "?floor=" + this.value;
    }
});

// FACILITY FILTER
$(".facility_filter").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("facility=") >= 0) {
            if (
                current_url.indexOf(",") >= 0 ||
                current_url.includes("search_term=")
            ) {
                if (current_url.includes("facility=,")) {
                    window.location.href = current_url.replace(
                        "facility=,",
                        "facility=" + this.value + ","
                    );
                } else {
                    window.location.href = current_url.replace(
                        /facility=/,
                        `facility=${this.value},`
                    );
                }
            } else {
                window.location.href = current_url + this.value + ",";
            }
        } else {
            window.location.href =
                current_url + "&facility=" + this.value + ",";
        }
    } else {
        window.location.href = current_url + "?facility=" + this.value + ",";
    }
});

// FACILITY FILTER CHECKED
$(".facility_filter_checked").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("facility=") >= 0) {
            if (current_url.includes(`${this.value},`)) {
                window.location.href = current_url.replace(
                    `${this.value},`,
                    ""
                );
            } else {
                window.location.href = current_url.replace(`${this.value}`, "");
            }
        } else {
            window.location.href = current_url + "&facility=" + "";
        }
    } else {
        window.location.href = current_url + "?facility=" + "";
    }
});

// EXTRA FACILITY FILTER
$(".extra_facility_filter").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("da=") >= 0) {
            if (current_url.indexOf(",") >= 0) {
                if (current_url.includes("da=,")) {
                    window.location.href = current_url.replace(
                        "da=,",
                        "da=" + this.value + ","
                    );
                } else {
                    window.location.href = current_url.replace(
                        /da=/,
                        `da=${this.value},`
                    );
                }
            } else {
                window.location.href = current_url + this.value + ",";
            }
        } else {
            window.location.href = current_url + "&da=" + this.value + ",";
        }
    } else {
        window.location.href = current_url + "?da=" + this.value + ",";
    }
});

// EXTRA FACILITY FILTER CHECKED
$(".extra_facility_filter_checked").on("change", function () {
    let current_url = window.location.pathname + window.location.search;
    if (current_url.indexOf("?") >= 0) {
        if (current_url.indexOf("da=") >= 0) {
            window.location.href = current_url.replace(`${this.value},`, "");
        } else {
            window.location.href = current_url + "&da=" + "";
        }
    } else {
        window.location.href = current_url + "?da=" + "";
    }
});

// Homepage Advance Filters
$(".advance_any_filter_button").on("click", function () {
    $(".advance_st").val($(".advance_any_status").val());
    $(".advance_search_term").val($(".advance_any_search_term").val());
    $(".advance_max_prd").val($(".advance_any_max_prc").val());
    $(".advance_cn").val($(".advance_any_city").val());
});

$(".advance_rent_filter_button").on("click", function () {
    $(".advance_st").val($(".advance_rent_status").val());
    $(".advance_search_term").val($(".advance_rent_search_term").val());
    $(".advance_max_prd").val($(".advance_rent_max_prc").val());
    $(".advance_cn").val($(".advance_rent_city").val());
});

$(".advance_sale_filter_button").on("click", function () {
    $(".advance_st").val($(".advance_sale_status").val());
    $(".advance_search_term").val($(".advance_sale_search_term").val());
    $(".advance_max_prd").val($(".advance_sale_max_prc").val());
    $(".advance_cn").val($(".advance_sale_city").val());
});

$(".advance_category").on("change", function () {
    let categoryValue = $(this).val();

    if (categoryValue === "residential") {
        $(".advance_rooms").removeClass("d-none");
        $(".advance_bathrooms").removeClass("d-none");
        $(".advance_floors").removeClass("d-none");
    } else if (categoryValue === "commercial") {
        $(".advance_rooms").addClass("d-none");
        $(".advance_bathrooms").removeClass("d-none");
        $(".advance_floors").removeClass("d-none");
    } else {
        $(".advance_rooms").addClass("d-none");
        $(".advance_bathrooms").addClass("d-none");
        $(".advance_floors").addClass("d-none");
    }

    rpc("/property/advance-filters", {
        category_value: categoryValue,
    }).then(function (result) {
        let text = '<option selected="selected">All Sub Categories</option>';
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

function add_amt_attribute(id, self, name) {
    if (self.checked) {
        $("#" + id).attr("name", "facility");
    } else {
        $("#" + id).removeAttr("name");
    }
}
