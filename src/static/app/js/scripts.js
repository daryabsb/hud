function renderDataTable(elId, ajaxUrl, options = {}) {
    var width = window.innerWidth;
    var table = document.getElementById(elId);
    var tablePageSizeButton = document.getElementById('page-size')

    fetch(ajaxUrl)
        .then(response => response.json())
        .then(data => {
            data.columns.unshift(
                {
                    data: null,
                    render: DataTable.render.select()
                },
                {
                    data: 'id',
                    title: '<i class="fa fa-search fa-fw"></i>',
                }
            )

            //console.log(data.columns);
            var formattedColumns = formatColumns(data.columns);

            table = new DataTable(table, {
                ordering: false,
                ajax: {
                    url: ajaxUrl,
                    dataSrc: 'data',
                },
                scrollX: true, // width - 335,
                fixedHeader: true,
                processing: true,
                columns: formattedColumns,
                serverSide: true,
                rowId: 'extn',
                pageLength: 10,
                lengthMenu: [10, 25, 50, 100],
                columnDefs: [
                    {
                        orderable: false,
                        render: DataTable.render.select(),
                        targets: 0
                    }
                ],
                select: {
                    style: 'os',
                    selector: 'td:first-child',
                    headerCheckbox: true,
                    //style: 'single',
                },
                layout: {
                    //top: toolbar,
                    topEnd: null,
                    topStart: null,
                    // topStart: {
                    //     buttons: [
                    //         {
                    //             extend: 'collection',
                    //             text: 'Export',
                    //             buttons: ['csv', 'excel', 'pdf']
                    //         }
                    //     ]
                    // }
                },
                ...options,
            });

            pageLengthOptions = table.settings().init().lengthMenu;

            pageLengthOptions.forEach(value => {
                const option = document.createElement('option');
                option.value = value;
                option.text = value;
                tablePageSizeButton.appendChild(option);
            });
            tablePageSizeButton.addEventListener('change', function () {
                const value = parseInt(this.value, 10);
                table.page.len(value).draw();
            });

            table.on('select', function (e, dt, type, indexes) {
                if (type === 'row') {
                    var data = table
                        .rows(indexes)
                        .data()
                        .pluck('id');
                    console.log("on-select = ", data[0]);
                    // do something with the ID of the selected items
                }
            });


            //console.log(table.settings().init().lengthMenu);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    var searchInput = document.getElementById('top-search')
    var selectAllButton = document.getElementById('select-all')
    var deSelectAllButton = document.getElementById('deselect-all')
    var reloadTableDataButton = document.getElementById('reload-table')
    var tablePageBackButton = document.getElementById('table-page-back')
    var tablePageNextButton = document.getElementById('table-page-next')




    searchInput.addEventListener('keyup', function (e) {
        table.search(this.value).draw();
    });
    selectAllButton.addEventListener('click', function (e) {
        table.rows().select();
    });
    deSelectAllButton.addEventListener('click', function (e) {
        table.rows().deselect();
    });
    reloadTableDataButton.addEventListener('click', function (e) {
        table.ajax.reload();
    });
    tablePageBackButton.addEventListener('click', function (e) {
        table.page('previous').draw(false);
    });
    tablePageNextButton.addEventListener('click', function (e) {
        table.page('next').draw(false);
    });

}

function getImage(data) {
    return `
        <div 
        _="on click alert 'my *width' end"
        class="w-20px h-20px bg-inverse bg-opacity-25 d-flex align-items-center justify-content-center">
            <img alt="" class="mw-100 mh-100" src="/media/${data}">
        </div>`
}
// Function to format columns
function formatColumns(columns) {
    //console.log("typeof columns: ", typeof columns)
    return columns.map(column => {
        if (column.title === '<i class="fa fa-search fa-fw"></i>') {
            return {
                ...column,
                render: function (data, type) {
                    if (type === 'display') {
                        return `<a href="#" data-bs-toggle="modal" data-bs-target="#modalDetail" id="${data}">
                                    <i class="fa fa-search fa-fw"></i>
                                </a>` // Remove trailing zeros
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
        if (column.data === 'image') {
            return {
                ...column,
                render: function (data, type) {
                    if (type === 'display') {
                        return getImage(data);
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

