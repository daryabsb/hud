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
            // columns1.unshift(
            //     {
            //         data: null,
            //         render: DataTable.render.select()
            //     },
            //     {
            //         data: 'id',
            //         title: '<i class="fa fa-search fa-fw"></i>',
            //     }
            // )
        })
        .catch(err => console.error('Error fetching data:', err))

    await fetch(ajaxUrl[1])
        .then(response => response.json())
        .then(data => {
            columns2 = data.columns
            // columns2.unshift(
            //     {
            //         data: null,
            //         render: DataTable.render.select()
            //     },
            //     {
            //         data: 'id',
            //         title: '<i class="fa fa-search fa-fw"></i>',
            //     }
            // )
        })
        .catch(err => console.error('Error fetching data:', err))

    var opts = {
        ordering: false,
        scrollX: true, // width - 335,
        fixedHeader: true,
        processing: true,
        serverSide: true,
        rowId: 'extn',
        language: {
            infoEmpty: 'No records to show!'
        },
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
            //selector: 'td:first-child',
            //headerCheckbox: true
        },
        layout: {
            //top: toolbar,
            bottomStart: null,
            bottomEnd: null,
            topEnd: null,
            topStart: null,
            bottomStart: {
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

    table1
        .on('select', function (e, dt, type, indexes) {
            if (type === 'row') {
                var data = table1
                    .rows(indexes)
                    .data()
                    .pluck('id');
                // do something with the ID of the selected items
                table2.ajax.url(
                    `/mgt/document-items-datatable/?document-id=${data[0]}&datatables=1`
                ).load() //= `{% url "mgt:document-items-datatable" %}?document-id=${data[0]}&datatables=1`
            }
        })
        .on('deselect', function (e, dt, type, indexes) {
            if (type === 'row') {
                var data = table1
                    .rows(indexes)
                    .data()
                    .pluck('id');
                // do something with the ID of the selected items
                table2.ajax.url(
                    `/mgt/document-items-datatable/?document-id=&datatables=1`
                ).load() //= `{% url "mgt:document-items-datatable" %}?document-id=${data[0]}&datatables=1`
            }
        });



    const minEl = document.querySelector('#start-date');
    const maxEl = document.querySelector('#end-date');
    const documentProductFilter = document.querySelector('#id_product');

    documentProductFilter.addEventListener('change', function (e) {
        console.log(e);

        table1.search(this.value).draw();
        table2.search(this.value).draw();
    });
    // table1.on('search.dt', function (searchStr, data) {
    //     console.log('searchStr = ', new Date(searchStr.timeStamp));
    //     console.log('data = ', new Date(data.api.data()[0].created));
    //     var min = new Date(minEl.value, 10);
    //     var max = new Date(maxEl.value, 10);
    //     var created = new Date(data.api.data()[0].created)
    //     if (
    //         (isNaN(min) && isNaN(max)) ||
    //         (isNaN(min) && created <= max) ||
    //         (min <= created && isNaN(max)) ||
    //         (min <= created && created <= max)
    //     ) {
    //         return true;
    //     }

    //     return false;



    // });

    table1.search.fixed('range', function (searchStr, data, index) {
        console.log(data);
        var age = parseFloat(data[20]) || 0; // use data for the age column

    });

    //Changes to the inputs will trigger a redraw to update the table
    minEl.addEventListener('input', function (e, d) {
        table1.search.fixed('range', function (e, d, index) {
            var min = parseInt(minEl.value, 10);
            var max = parseInt(maxEl.value, 10);
            var age = parseFloat(d[20]) || 0; // use data for the age column

            if (
                (isNaN(min) && isNaN(max)) ||
                (isNaN(min) && age <= max) ||
                (min <= age && isNaN(max)) ||
                (min <= age && age <= max)
            ) {
                return true;
            }

            return false;
        });

    });
    maxEl.addEventListener('input', function (e, d) {
        table1
            .search(e, d)
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
            || column.data === 'returned'
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

