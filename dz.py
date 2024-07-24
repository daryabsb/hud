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
            f"{app}/plugins/toastify/toastify.min.css",
        ],
        "global_js": {
            "top": [
                f"{app}/js/vendor.min.js",
                f"{app}/js/app.min.js",
                # f"{app}/plugins/jquery/jquery.min.js",
                f"{app}/plugins/jscolor/jscolor.min.js",
                f"{app}/plugins/toastify/toastify-js.js",
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
                "mgt_price_tags": [
                    # f"{app}/plugins/photoswipe/dist/photoswipe.css",
                    # f"{app}/plugins/pdfjs/web/viewer.css",

                ],
                "mgt_price_tags_control": [
                    f"{app}/css/price-tags.css",


                ],
                "mgt_documents": [
                    # f"{app}/plugins/select2/dist/select2.min.css",
                    f"{app}/plugins/datatable/datatables.min.css",
                    # f"{app}/plugins/datatables.net-bs5/css/dataTables.bootstrap5.min.css",
                    # f"{app}/plugins/datatables.net-responsive-bs5/css/responsive.bootstrap5.min.css",
                    # f"{app}/plugins/datatables.net-fixedcolumns-bs5/css/fixedColumns.bootstrap5.min.css",
                    # f"{app}/plugins/datatables.net-buttons-bs5/css/buttons.bootstrap5.min.css",
                    # f"{app}/plugins/select2/dist/select2.min.css",
                    # f"{app}/plugins/bootstrap-daterangepicker/bootstrap-datepicker.min.css",
                ],
                "mgt_users": [
                    # f"{app}/plugins/tag-it/js/tag-it.min.js",

                ],
            },
            "js": {
                "pos_home": [
                    f"{app}/js/demo/pos-customer-order.demo.js",
                ],
                "mgt_documents": [
                    # f"{app}/plugins/datatable/datatables.min.js",
                    # f"{app}/plugins/datatables.net/js/dataTables.min.js",
                    # f"{app}/plugins/datatables.net-bs5/js/dataTables.bootstrap5.min.js",
                    # f"{app}/plugins/datatables.net-buttons/js/dataTables.buttons.min.js",
                    # f"{app}/plugins/jszip/dist/jszip.min.js",
                    # f"{app}/plugins/pdfmake/build/pdfmake.min.js",
                    # f"{app}/plugins/pdfmake/build/vfs_fonts.js",
                    # f"{app}/plugins/datatables.net-buttons/js/buttons.colVis.min.js",
                    # f"{app}/plugins/datatables.net-buttons/js/buttons.html5.min.js",
                    # f"{app}/plugins/datatables.net-buttons/js/buttons.print.min.js",
                    # f"{app}/plugins/datatables.net-buttons-bs5/js/buttons.bootstrap5.min.js",
                    # f"{app}/plugins/datatables.net-responsive/js/dataTables.responsive.min.js",
                    # f"{app}/plugins/datatables.net-responsive-bs5/js/responsive.bootstrap5.min.js",
                    # f"{app}/plugins/datatables.net-fixedcolumns/js/dataTables.fixedColumns.min.js",
                    # f"{app}/plugins/datatables.net-fixedcolumns-bs5/js/fixedColumns.bootstrap5.min.js",
                    # f"{app}/js/demo/page-data-management.demo.js",
                    # f"{app}/plugins/select2/dist/select2.min.js",
                    # f"{app}/plugins/moment/moment.js",
                    # f"{app}/plugins/bootstrap-daterangepicker/bootstrap-datepicker.min.js",
                    # f"{app}/js/demo/daterange.js",
                    # f"{app}/plugins/jquery-migrate/dist/jquery-migrate.min.js",
                    # f"{app}/plugins/moment/min/moment.min.js",
                    # f"{app}/plugins/select-picker/dist/picker.min.js",
                    # f"{app}/js/demo/form-plugins.demo.js",
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
                ],
                "mgt_users": [
                    # f"{app}/plugins/jquery-migrate/dist/jquery-migrate.min.js",
                    # f"{app}/plugins/tag-it/js/tag-it.min.js",
                ],
            },
        }
    }
}
