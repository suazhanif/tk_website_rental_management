/** @odoo-module */
import { loadJsFile } from "../plugin_loader.js";
(async function () {
    await loadJsFile("/tk_website_rental_management/static/src/js/plugins.js");
})();

function lazyLoading() {
    /**
     * Initialization of lazy loading
     */
    $(".dynamic-tab").removeClass("home-skeleton");

    var lazyImages = [].slice.call(document.querySelectorAll("img.lazy"));

    if ("IntersectionObserver" in window) {
        let lazyImageObserver = new IntersectionObserver(function (
            entries,
            observer
        ) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    let lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove("lazy");
                    lazyImageObserver.unobserve(lazyImage);

                    setInterval(function () {
                        if (
                            lazyImage.parentElement.classList.contains(
                                "skeleton"
                            )
                        ) {
                            lazyImage.parentElement.classList.remove(
                                "skeleton"
                            );
                        } else {
                            lazyImage.parentElement.classList.remove(
                                "property-skeleton"
                            );
                        }
                    }, 1500);
                }
            });
        });

        lazyImages.forEach(function (lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    } else {
        setInterval(function () {
            let images = document.querySelectorAll("img");
            images.forEach((lazyImage) => {
                if (lazyImage.classList.contains("lazy")) {
                    lazyImage.setAttribute(
                        "src",
                        lazyImage.getAttribute("data-src")
                    );
                    if (
                        lazyImage.parentElement.classList.contains("skeleton")
                    ) {
                        lazyImage.parentElement.classList.remove("skeleton");
                    } else {
                        lazyImage.parentElement.classList.remove(
                            "property-skeleton"
                        );
                    }
                }
            });
        }, 1500);
    }
}

function initIsotope() {
    /**
     * Initialization of Isotope for images and gallery items
     */
    if ($(".gallery-items").length) {
        var ami = $(".gallery-items").isotope({
            singleMode: true,

            itemSelector:
                ".gallery-item, .gallery-item-second, .gallery-item-three",
            transformsEnabled: true,
            transitionDuration: "700ms",
            resizable: true,
        });
        ami.imagesLoaded(function () {
            ami.isotope("layout");
        });
        $(".gallery-filters").on("click", "a.gallery-filter", function (a) {
            a.preventDefault();
            var brec = $(this).attr("data-filter");
            ami.isotope({
                filter: brec,
            });
            $(".gallery-filters a").removeClass("gallery-filter-active");
            $(this).addClass("gallery-filter-active");
        });
    }
    if ($(".restor-menu-widget").length) {
        var aresm = $(".restor-menu-widget").isotope({
            singleMode: true,
            itemSelector: ".restmenu-item",
            transformsEnabled: true,
            transitionDuration: "700ms",
            resizable: true,
        });
        aresm.imagesLoaded(function () {
            aresm.isotope("layout");
        });
        $(".menu-filters").on("click", "a", function (a) {
            a.preventDefault();
            var brec = $(this).attr("data-filter");
            aresm.isotope({
                filter: brec,
            });
            $(".menu-filters a").removeClass("menu-filters-active");
            $(this).addClass("menu-filters-active");
        });
    }
}

function matchHeight() {
    /**
     * For cards align equal height
     */
    $(".listing-item").matchHeight({});
    $(".geodir-category-content").matchHeight({});
    $(".geodir-category-content-title").matchHeight({});
    $(".geodir-category-text").matchHeight({});
    $(".geodir-category-footer").matchHeight({});
    $(".small-text").matchHeight({});
    $(".facilities-list").matchHeight({});
    $(".gallery-item").matchHeight({});
    $(".article-masonry").matchHeight({});
}

function initHiddenGal(data) {
    /**
     * Initialization of dynamic gallery
     */
    $(".snippets-gal").on("click", async function () {
        var access_token = $(this).attr("data-dynamicPath");
        let dynamicgal;
        await data.popular_listing.map((e, i) => {
            if (e.access_token === access_token) {
                dynamicgal = e.property_images;
            }
        });
        $(this).lightGallery({
            dynamic: true,
            dynamicEl: dynamicgal,
            download: false,
            loop: false,
            counter: false,
        });
    });
}

export { lazyLoading, initIsotope, matchHeight, initHiddenGal };
