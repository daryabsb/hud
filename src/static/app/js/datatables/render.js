// Function to format columns

async function renderDataTable(elId, inputId, ajaxUrl, options = {}) {
    var table = document.getElementById(elId);
    var columns1 = await fetchData(ajaxUrl);
    var formattedColumns = await formatColumns(columns1);

    // Initialize DataTable
    table = new DataTable(table, {
        ajax: {
            url: ajaxUrl,
            type: 'GET', // Match backend's use of request.GET
            data: function (d) {
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
        pageLength: options.pageLength || 5, // Default page size
        layout: {
            bottomStart: {
                pageLength: {
                    menu: [5, 10, 25, 50, 100]
                }
            },
            // topStart: 'info',
            bottomEnd: 'paging'
        },
        columns: formattedColumns,
        columnDefs: [
            { targets: [1, 2], visible: false },
            { targets: '_all', visible: true }
        ],
        createdRow: function (row, data, dataIndex) {
            // Add the data-id attribute to the <tr>
            row.setAttribute('data-id', data.id);
            row.setAttribute('hx-get', `/pos/modal-product/${data.id}/`);
            row.setAttribute('hx-target', '#modalProduct');
            row.setAttribute('hx-trigger', 'click');
            row.setAttribute('data-bs-toggle', 'modal');
            row.setAttribute('data-bs-target', '#modalProduct');
        },
        ...options, // Allow user overrides
    });
    // Bind search input
    table
        .on('draw.dt', function () {
            htmx.process(document.body);
        });
    var searchInput = document.getElementById(inputId);
    searchInput.addEventListener('keyup', function (e) {
        table.search(this.value).draw();
    });




}

