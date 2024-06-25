app = 'app'
htmx = 'htmx'

dz_array = {
    "public": {
        "favicon": f"{app}/images/favicon.png",
        "description": "W3CMS  : Django CMS With Dashboard & FrontEnd Template",
        "og_title": "W3CMS  : Django CMS With Dashboard & FrontEnd Template",
        "og_description": "W3CMS  : Django CMS With Dashboard & FrontEnd Template",
        "og_image": "https://w3cms.dexignzone.com/django/social-image.png",
        "title": "W3CMS  : Django CMS With Dashboard & FrontEnd Template",
    },

    "app": {
        "htmx": [
            f"{htmx}/htmx.min.js",
            f"{htmx}/class-tools.js",
            f"{htmx}/preload.js",
            f"{htmx}/_hyperscript.js",
            f"{htmx}/ext/debug.js",
            f"{htmx}/ext/event-header.js",
        ],
        "global_css": [
            f"{app}/css/vendor.min.css",
            f"{app}/css/app.min.css",
        ],
        "global_js": {
            "top": [
                f"{app}/js/vendor.min.js",
                f"{app}/js/app.min.js",
            ],
            "down": [
                f"{app}/js/rocket-loader.min.js",
            ],
        },
        "page_level": {
            "css": {
                "pos_home": [

                ],
                "mgt_products": [
                    f"{app}/plugins/bootstrap-icons/font/bootstrap-icons.css",

                ],
                "mgt_users": [
                    # f"{app}/plugins/tag-it/js/tag-it.min.js",

                ],
            },
            "js": {
                "pos_home": [
                    f"{app}/js/demo/pos-customer-order.demo.js",
                ],
                "mgt_products": [
                    f"{app}/plugins/iconify/iconify.min.js",
                    f"{app}/js/demo/file-manager.demo.js",
                ],
                "mgt_users": [
                    # f"{app}/plugins/jquery-migrate/dist/jquery-migrate.min.js",
                    # f"{app}/plugins/tag-it/js/tag-it.min.js",
                ],
            },
        }
    }
}
