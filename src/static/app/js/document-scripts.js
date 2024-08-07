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

function format(d) {
    return (
        'Internal Note: ' +
        d.internal_note +
        '<br>' +
        'Note: ' +
        d.note +
        '<br>' +
        'The child row can contain any data you wish, including links, images, inner tables etc.'
    );
}
Object.assign(DataTable.defaults, {
    ordering: false,
    scrollX: true, // width - 335,
    scrollY: 180,
    fixedHeader: true,
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
        topEnd: null,
        topStart: null,
        topEnd: null,
    },
});

async function renderDocumentsDataTable(elId = [], ajaxUrl = [], options = {}) {
    var table1 = document.getElementById(elId[0]); var table2 = document.getElementById(elId[1]); var columns1; var columns2;

    await fetch(ajaxUrl[0])
        .then(response => response.json())
        .then(data => {
            columns1 = data.columns;
            columns1.unshift(
                {
                    class: 'dt-control',
                    orderable: false,
                    data: null,
                    defaultContent: '',
                    //render: DataTable.render.select()
                },
            )

        })
        .catch(err => console.error('Error fetching data:', err))

    await fetch(ajaxUrl[1])
        .then(response => response.json())
        .then(data => {
            columns2 = data.columns
        })
        .catch(err => console.error('Error fetching data:', err))

    var formattedColumns1 = formatColumns(columns1);
    var formattedColumns2 = formatColumns(columns2);

    table1 = new DataTable(table1, {
        ...options,
        ajax: {
            url: ajaxUrl[0],
            dataSrc: 'data',
        },
        columns: formattedColumns1,
    });
    table2 = new DataTable(table2, {
        ...options,
        ajax: {
            url: ajaxUrl[1],
            dataSrc: 'data',
        },
        columns: formattedColumns2,
    });

    // Array to track the ids of the details displayed rows
    const detailRows = [];

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
        })
        .on('click', 'tbody td.dt-control', function (event) {
            let tr = event.target.closest('tr');
            let row = table1.row(tr);
            let idx = detailRows.indexOf(tr.id);

            if (row.child.isShown()) {
                tr.classList.remove('details');
                row.child.hide();

                // Remove from the 'open' array
                detailRows.splice(idx, 1);
            }
            else {
                tr.classList.add('details');
                row.child(format(row.data())).show();

                // Add to the 'open' array
                if (idx === -1) {
                    detailRows.push(tr.id);
                }
            }
        })
        .on('draw', () => {
            detailRows.forEach((id, i) => {
                let el = document.querySelector('#' + id + ' td.dt-control');
                if (el) {
                    el.dispatchEvent(new Event('click', { bubbles: true }));
                }
            });
        });



    const minEl = document.querySelector('#start-date');
    const maxEl = document.querySelector('#end-date');



    var document_filter_forms_buttons = [
        document.querySelector('#id_product'),
        document.querySelector('#id_user'),
        document.querySelector('#id_document_type'),
        document.querySelector('#id_paid_status'),
        document.querySelector('#id_customer'),
    ]
    document_filter_forms_buttons.forEach(button => {
        if (button) { // Check if the element exists
            button.addEventListener('change', function (e) {
                table1.search(this.value).draw(); // Ensure table2 is defined and accessible
            });
        }
    });



    // const documentProductFilter = document.querySelector('#id_product');
    // const documentUserFilter = document.querySelector('#id_user');
    // const documentTypeFilter = document.querySelector('#id_document_type');
    // const documentPaidStatusFilter = document.querySelector('#id_paid_status');
    // const documentCustomerFilter = document.querySelector('#id_customer');
    // documentProductFilter.addEventListener('change', function (e) {
    //     table2.search(this.value).draw();
    // });
    // documentUserFilter.addEventListener('change', function (e) {
    //     table2.search(this.value).draw();
    // });
    // documentTypeFilter.addEventListener('change', function (e) {
    //     table1.search(this.value).draw();
    // });
    // documentPaidStatusFilter.addEventListener('change', function (e) {
    //     table1.search(this.value).draw();
    // });
    // documentCustomerFilter.addEventListener('change', function (e) {
    //     table1.search(this.value).draw();
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
    const documentCSVButton = document.querySelector('#export-csv');
    const documentExcelButton = document.querySelector('#export-excel');
    const documentPdfButton = document.querySelector('#export-pdf');
    documentCSVButton.addEventListener('click', function (e, d) {
        table1.button(0).trigger();
    });
    documentExcelButton.addEventListener('click', function (e, d) {
        table1.button(1).trigger();
    });
    documentPdfButton.addEventListener('click', function (e, d) {
        console.log('PDF Triggered', table1.button(0).text());
        table1.button(2).trigger();
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


// columnDefs: [
//     {
//         orderable: false,
//         render: DataTable.render.select(),
//         targets: 0
//     }
// ],

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




// topEnd: {
//     buttons: [
//         {
//             extend: 'collection',
//             text: 'Export',
//             buttons: [
//                 'csv',
//                 'excel',
//                 {
//                     extend: 'pdf',
//                     text: 'Save PDF',
//                     title: 'Documents',
//                     filename: `Documents-${new Date()}`,
//                     orientation: 'landscape',
//                     pageSize: 'A3',
//                     exportOptions: {
//                         modifier: {
//                             //page: 'current',
//                             columns: 'all'
//                         },
//                     }
//                 },
//             ]
//         }
//     ]
// }