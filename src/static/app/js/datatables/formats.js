Object.assign(DataTable.defaults, {
    ordering: false,
    scrollX: true, // width - 335,
    scrollY: 225,
    // fixedHeader: {
    //     header: false,
    //     footer: true,
    // },
    processing: true,
    compact: true,
    serverSide: true,
    rowId: 'extn',
    // select: {
    //     style: 'os',
    // },
    select: false,
    buttons: getButtons(),
    // pageLength: 5,
    //lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]], // Page size options

    lengthMenu: [10, 25, 50, 100],
    layout: {
        //top: toolbar,
        bottomStart: null,
        bottomEnd: null,
        topEnd: 'paging',
        topStart: null,
        topEnd: null,
    },
    deferRender: true, // Optimize for large datasets
    fixedHeader: true,
    language: {
        emptyTable: 'No data available. Try searching for a product.',
        processing: 'Loading...',
    },
});

async function formatColumns(columns) {
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
        if (column.data === 'actions') {
            return {
                ...column,
                render: function (data, type, row) {
                    if (type === 'display') {
                        return getActions(data, row);
                    }
                }
            }
        }

        return column; // Return column unchanged if no modification
    });
}
