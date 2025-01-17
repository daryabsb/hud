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
            f"{app}/css/style.css",
            f"{app}/plugins/toastify/toastify.min.css",
            f"{app}/plugins/datatable/datatables.min.css",
            f"{app}/plugins/datatable/data-tables.css",
        ],
        "global_js": {
            "top": [
                f"{app}/js/vendor.min.js",
                f"{app}/js/app.min.js",
                f"{app}/plugins/datatable/datatables.min.js",
                # f"{app}/plugins/jquery/jquery.min.js",
                f"{app}/plugins/jscolor/jscolor.min.js",
                f"{app}/plugins/toastify/toastify-js.js",
                # f"{app}/js/render-datatable.js",

            ],
            "down": [
                f"{app}/js/rocket-loader.min.js",
                f"{app}/js/scripts.js",
            ],
        },
        "page_level": {
            "css": {
                "pos_home": [
                ],
                "mgt_products": [
                    f"{app}/plugins/bootstrap-icons/font/bootstrap-icons.css",

                ],
                "mgt_price_tags": [
                    # f"{app}/plugins/photoswipe/dist/photoswipe.css",
                    # f"{app}/plugins/pdfjs/web/viewer.css",

                ],
                "mgt_price_tags_control": [
                    f"{app}/css/price-tags.css",


                ],


                "mgt_documents": [
                    # f"{app}/plugins/select2/dist/css/select2.min.css",
                    # f"{app}/plugins/select2-bootstrap-5-theme/select2-bootstrap-5-theme.min.css",
                    # f"{app}/plugins/select2-bootstrap-5-theme/select2-bootstrap-5-theme.rtl.min.css",

                ],
                "mgt_users": [
                    # f"{app}/plugins/tag-it/js/tag-it.min.js",

                ],
            },
            "js": {
                "pos_home": [
                    f"{app}/plugins/interactjs/dist/interact.js",
                    f"{app}/js/demo/pos-customer-order.demo.js",
                ],
                "mgt_documents": [
                    # f"{app}/plugins/jquery-slim/jquery.slim.min.js",
                    # f"{app}/plugins/select2/dist/js/select2.full.min.js",
                    f"{app}/js/document-scripts.js",
                    f"{app}/js/demo/file-manager.demo.js",
                ],
                "mgt_orders": [
                    # f"{app}/plugins/jquery-slim/jquery.slim.min.js",
                    # f"{app}/plugins/select2/dist/js/select2.full.min.js",
                    f"{app}/js/document-scripts.js",
                    f"{app}/js/demo/file-manager.demo.js",
                ],
                "document_list": [
                    f"{app}/js/document-scripts.js",
                    f"{app}/js/demo/file-manager.demo.js",
                ],
                "document_list_view": [
                    f"{app}/js/document-scripts.js",
                    f"{app}/js/demo/file-manager.demo.js",
                ],
                "mgt_price_tags": [

                    # f"{app}/plugins/pdfjs/popper.min.js",
                    # f"{app}/plugins/pdfjs/pdf.min.js",
                    # f"{app}/plugins/pdfjs/pdf.worker.mjs",
                ],
                "mgt_price_tags_control": [

                ],
                "mgt_products": [
                    f"{app}/plugins/iconify/iconify.min.js",
                    f"{app}/js/demo/file-manager.demo.js",
                    # f"{app}/js/mgt/products-client.js",

                ],
                "view": [
                    # f"{app}/plugins/iconify/iconify.min.js",
                    # f"{app}/js/demo/file-manager.demo.js",
                    # f"{app}/js/mgt/products-client.js",

                ],
                "mgt_users": [
                    # f"{app}/plugins/jquery-migrate/dist/jquery-migrate.min.js",
                    # f"{app}/plugins/tag-it/js/tag-it.min.js",
                ],
            },
        }
    }
}
