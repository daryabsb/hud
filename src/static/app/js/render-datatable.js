// Function to format columns
function formatColumns(columns) {
    //console.log("typeof columns: ", typeof columns)

    return columns.map(column => {

        // if (column.title === '<i class="fa fa-search fa-fw"></i>') {
        if (column.data === 'id') {
            return {
                ...column,
                render: function (data, type, row) {
                    if (type === 'display') {
                        return getCode(data, row) // Remove trailing zeros
                    }
                    return data;
                }
            };
        }

        if (column.data === 'price') {
            return {
                ...column,
                render: function (data, type) {
                    if (type === 'display') {
                        return parseFloat(data).toString(); // Remove trailing zeros
                    }
                    return data;
                }
            };
        }
        if (column.data === 'created' || column.data === 'updated') {
            return {
                ...column,
                render: function (data, type) {
                    if (type === 'display') {
                        let date = new Date(data);
                        return date.toLocaleString(); // Format the date
                    }
                    return data;
                }
            };
        }
        if (column.data === 'name') {

            return {
                ...column,
                render: function (data, type, row) {
                    if (type === 'display') {
                        return getName(data, row);
                    }
                }
            };
        }

        if (column.data === 'color') {
            return {
                ...column,
                render: function (data, type) {
                    if (type === 'display') {
                        return `<div class="w-20px h-20px" style="background-color: ${data};"></div>`
                    }
                }
            };
        }

        if (
            column.data === 'is_tax_inclusive_price'
            || column.data === 'is_enabled'
            || column.data === 'is_price_change_allowed'
            || column.data === 'is_service'
            || column.data === 'is_using_default_quantity'
        ) {
            return {
                ...column,
                render: function (data, type) {
                    if (type === 'display') {
                        if (data == false) {
                            return `<i class="text-danger bi-check-circle-fill"></i>`;
                        } else {
                            return `<i class="text-success bi-check-circle-fill"></i>`;
                        }
                    }
                    return data;
                }
            };
        }

        return column; // Return column unchanged if no modification
    });
}

async function renderDataTable(elId, inputId, ajaxUrl, options = {}) {
    var table = document.getElementById(elId);
    var columns1;

    // Initial fetch to get column definitions
    await fetch(ajaxUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Initial data:', data.data);
            columns1 = data.columns;
            //columns1[0].class = 'btn btn-outline-theme text-success'
            indexes1 = data.indexes

            // Format columns from server response




        })
        .catch(error => {
            console.error('Error initializing table:', error);
            alert('Failed to initialize table. Please check the server connection.');
        });

    var formattedColumns = formatColumns(columns1);

    // Initialize DataTable
    table = new DataTable(table, {
        ordering: false,
        ajax: {
            url: ajaxUrl,
            type: 'GET', // Match backend's use of request.GET
            data: function (d) {
                // Send parameters expected by Django view
                return {
                    draw: d.draw,
                    start: d.start,
                    length: d.length,
                    'search[value]': d.search.value,
                };
            },
            dataSrc: 'data',
            error: function (xhr, error, thrown) {
                console.error('AJAX error:', error, thrown);
                alert('Failed to load table data. Please try again.');
            }
        },
        deferRender: true, // Optimize for large datasets
        scrollY: 225,
        fixedHeader: true,
        processing: true,
        serverSide: true,
        columns: formattedColumns,
        select: true,
        pageLength: options.pageLength || 5, // Default page size
        //lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]], // Page size options
        layout: {
            bottomStart: {
                pageLength: {
                    menu: [5, 10, 25, 50, 100]
                }
            },
            // topStart: 'info',
            bottomEnd: 'paging'
        },
        language: {
            emptyTable: 'No data available. Try searching for a product.',
            processing: 'Loading...',
        },
        columnDefs: [
            { targets: [1, 2], visible: false },
            { targets: '_all', visible: true }
        ],
        ...options, // Allow user overrides
    });
    // Bind search input
    var searchInput = document.getElementById(inputId);
    searchInput.addEventListener('keyup', function (e) {
        table.search(this.value).draw();
    });
}

function getImage(data, row) {
    return `
        <div class="d-flex align-items-center">
            <div class="w-50px h-50px bg-inverse bg-opacity-25 d-flex align-items-center justify-content-center">
                <img alt="" class="mw-100 mh-100" src="/media/${data}">
            </div>
            <div class="ms-3">
                <a href="page_product_details.html" class="text-inverse text-opacity-75 text-decoration-none">${row.name}</a>
            </div>
        </div>`
}

function getCode(data, row) {
    return `
        <div class="form-check d-flex align-items-center">
            <input type="checkbox" class="form-check-input" id="${data}">
            <label class="form-check-label" for="${data}">${row.code}</label>
        </div>
    `
}

function getName(data, row) {
    return `
        <div class="d-flex align-items-center">
            <div class="w-50px h-50px bg-inverse bg-opacity-25 d-flex align-items-center justify-content-center">
                <img alt="" class="mw-100 mh-100" src="/media/${row.image}">
            </div>
            <div class="ms-3">
                <a href="page_product_details.html" class="text-inverse text-opacity-75 text-decoration-none">${data}</a>
            </div>
        </div>`
}

function getRow(data, row) {
    return `<tr>
                <td class="w-10px align-middle">
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="${data}">
                        <label class="form-check-label" for="product1">${row.code}</label>
                    </div>
                </td>
                <td>
                    <div class="d-flex align-items-center">
                        <div class="w-50px h-50px bg-inverse bg-opacity-25 d-flex align-items-center justify-content-center">
                            <img alt="" class="mw-100 mh-100" src="/media/${row.image}">
                        </div>
                        <div class="ms-3">
                            <a href="page_product_details.html" class="text-inverse text-opacity-75 text-decoration-none">${row.name}</a>
                        </div>
                    </div>
                </td>
                <td class="align-middle">${row.price}</td>
                <td class="align-middle">${row.parent_group}</td>
                <td class="align-middle">Force Majeure</td>
            </tr>`
}

function getButtons() {
    return [
        {
            extend: 'csv',
            text: `Save csv`,
            title: 'Documents',
            filename: `Documents-${new Date()}`,
            orientation: 'landscape',
            pageSize: 'A3',
            exportOptions: {
                modifier: {
                    //page: 'current',
                    columns: 'all'
                },
            }
        },
        {
            extend: 'excel',
            text: `Save Excel`,
            title: 'Documents',
            filename: `Documents-${new Date()}`,
            orientation: 'landscape',
            pageSize: 'A3',
            exportOptions: {
                modifier: {
                    //page: 'current',
                    columns: 'all'
                },
            }
        },
        {
            extend: 'pdf',
            text: `Save PDF`,
            title: 'Documents',
            filename: `Documents-${new Date()}`,
            orientation: 'landscape',
            pageSize: 'A3',
            exportOptions: {
                modifier: {
                    //page: 'current',
                    columns: 'all'
                },
            }
        },
    ]

}

Object.assign(DataTable.defaults, {
    ordering: false,
    scrollX: true, // width - 335,
    scrollY: 180,
    // fixedHeader: {
    //     header: false,
    //     footer: true,
    // },
    processing: true,
    compact: true,
    serverSide: true,
    rowId: 'extn',
    select: {
        style: 'os',
    },
    buttons: getButtons(),
    pageLength: 5,
    lengthMenu: [10, 25, 50, 100],
    layout: {
        //top: toolbar,
        bottomStart: null,
        bottomEnd: null,
        topEnd: 'paging',
        topStart: null,
        topEnd: null,
    },
});

/*

<tr>
    <td class="w-10px align-middle">
        <div class="form-check">
            <input type="checkbox" class="form-check-input" id="product1">
            <label class="form-check-label" for="product1"></label>
        </div>
    </td>
    <td>
        <div class="d-flex align-items-center">
            <div class="w-50px h-50px bg-inverse bg-opacity-25 d-flex align-items-center justify-content-center">
                <img alt="" class="mw-100 mh-100" src="assets/img/product/product-6.jpg">
            </div>
            <div class="ms-3">
                <a href="page_product_details.html" class="text-inverse text-opacity-75 text-decoration-none">Force Majeure White T Shirt</a>
            </div>
        </div>
    </td>
    <td class="align-middle">83 in stock for 3 variants</td>
    <td class="align-middle">Cotton</td>
    <td class="align-middle">Force Majeure</td>
</tr>

*/
var rowHtml = function (data, row) {
    return `<tr>
    <td class="w-10px align-middle">
        <div class="form-check">
            <input type="checkbox" class="form-check-input" id="${data}">
            <label class="form-check-label" for="product1">${row.code}</label>
        </div>
    </td>
    <td>
        <div class="d-flex align-items-center">
            <div class="w-50px h-50px bg-inverse bg-opacity-25 d-flex align-items-center justify-content-center">
                <img alt="" class="mw-100 mh-100" src="/media/${row.image}">
            </div>
            <div class="ms-3">
                <a href="page_product_details.html" class="text-inverse text-opacity-75 text-decoration-none">${row.name}</a>
            </div>
        </div>
    </td>
    <td class="align-middle">${row.price}</td>
    <td class="align-middle">${row.parent_group}</td>
    <td class="align-middle">Force Majeure</td>
</tr>`
}