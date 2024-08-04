async function renderDocumentsDataTable(elId = [], ajaxUrl = [], options = {}) {
    console.log(elId);
    console.log(ajaxUrl);
    var table1 = document.getElementById(elId[0]);
    var table2 = document.getElementById(elId[1]);

    var columns1;
    var columns2;

    await fetch(ajaxUrl[0])
        .then(response => response.json())
        .then(data => {
            columns1 = data.columns;
            console.log('column1 = ', columns1);

            columns1.unshift(
                {
                    data: null,
                    render: DataTable.render.select()
                },
                {
                    data: 'id',
                    title: '<i class="fa fa-search fa-fw"></i>',
                }
            )
        })
        .catch(err => console.error('Error fetching data:', err))

    await fetch(ajaxUrl[1])
        .then(response => response.json())
        .then(data => {
            columns2 = data.columns
            console.log(columns2);

            columns2.unshift(
                {
                    data: null,
                    render: DataTable.render.select()
                },
                {
                    data: 'id',
                    title: '<i class="fa fa-search fa-fw"></i>',
                }
            )
        })
        .catch(err => console.error('Error fetching data:', err))

    var opts = {
        ordering: false,
        scrollX: true, // width - 335,
        fixedHeader: true,
        processing: true,
        serverSide: true,
        rowId: 'extn',
        pageLength: 5,
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
            headerCheckbox: true
        },
        layout: {
            //top: toolbar,
            bottomStart: null,
            bottomEnd: null,
            topEnd: null,
            topStart: null,
            topStart: {
                buttons: [
                    {
                        extend: 'collection',
                        text: 'Export',
                        buttons: ['csv', 'excel', 'pdf']
                    }
                ]
            }
        },
        ...options,
    }

    var formattedColumns1 = formatColumns(columns1);
    var formattedColumns2 = formatColumns(columns2);

    table1 = new DataTable(table1, {
        ...opts,
        ajax: {
            url: ajaxUrl[0],
            dataSrc: 'data',
        },
        columns: formattedColumns1,
    });
    table2 = new DataTable(table2, {
        ...opts,
        ajax: {
            url: ajaxUrl[1],
            dataSrc: 'data',
        },
        columns: formattedColumns2,
    });

    table1.on('select', function (e, dt, type, indexes) {
        if (type === 'row') {
            var data = table1
                .rows(indexes)
                .data()
                .pluck('id');
            console.log("on-select = ", data[0]);
            // do something with the ID of the selected items
            table2.ajax.url(
                `{% url "mgt:document-items-datatable" %}?document-id=${data[0]}&datatables=1`
            ).draw() //= `{% url "mgt:document-items-datatable" %}?document-id=${data[0]}&datatables=1`
            console.log(table2.ajax.url())

        }
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

