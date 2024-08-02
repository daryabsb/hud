console.log(productListUrl);
/*
var columns_from_table =  [
    {'data': 'barcode', 'title': 'Barcode'}, 
    {'data': 'id', 'title': 'Id'}, 
    {'data': 'user', 'title': 'User'}, 
    {'data': 'name', 'title': 'Name'}, 
    {'data': 'slug', 'title': 'Slug'}, {'data': 'parent_group', 'title': 'Parent Group'}, {'data': 'code', 'title': 'Code'}, {'data': 'description', 'title': 'Description'}, {'data': 'plu', 'title': 'Plu'}, {'data': 'measurement_unit', 'title': 'Measurement Unit'}, {'data': 'price', 'title': 'Price'}, {'data': 'currency', 'title': 'Currency'}, {'data': 'is_tax_inclusive_price', 'title': 'Is Tax Inclusive Price'}, {'data': 'is_price_change_allowed', 'title': 'Is Price Change Allowed'}, {'data': 'is_service', 'title': 'Is Service'}, {'data': 'is_using_default_quantity', 'title': 'Is Using Default Quantity'}, {'data': 'is_product', 'title': 'Is Product'}, {'data': 'cost', 'title': 'Cost'}, {'data': 'margin', 'title': 'Margin'}, {'data': 'image', 'title': 'Image'}, {'data': 'color2', 'title': 'Color2'}, {'data': 'color', 'title': 'Color'}, {'data': 'is_enabled', 'title': 'Is Enabled'}, {'data': 'age_restriction', 'title': 'Age Restriction'}, {'data': 'last_purchase_price', 'title': 'Last Purchase Price'}, {'data': 'rank', 'title': 'Rank'}, {'data': 'created', 'title': 'Created'}, {'data': 'updated', 'title': 'Updated'}]
*/
var width = window.innerWidth;
let table;
document.addEventListener('DOMContentLoaded', function () {
    var table = document.getElementById('products-table');
    fetch(productListUrl)
        .then(response => response.json())
        .then(data => {
            //console.log('data = ', data.data)
            var formattedColumns = formatColumns(JSON.parse(columns).map(col => ({
                data: col.name,
                title: col.title
            })));
            let toolbar = document.createElement('div');
            toolbar.innerHTML = topToolbar // '<b>Custom tool bar! Text/images etc.</b>';
            table = new DataTable(table, {
                ordering: false,
                ajax: {
                    url: productListUrl,
                    dataSrc: 'data',
                },
                scrollX: true, // width - 335,
                fixedHeader: true,
                processing: true,
                columns: formattedColumns,
                serverSide: true,
                select: true,
                layout: {
                    //top: toolbar,
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
                }
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    // searchInput.addEventListener('input', function (e) {
    //     table.search(e.target.value).draw();
    // })
    var searchInput = document.getElementById('top-search')
    searchInput.addEventListener('keyup', function (e) {

        console.log(e)
        table.search(this.value).draw();
    })

});


function getImage(data) {
    return `
        <div class="w-20px h-20px bg-inverse bg-opacity-25 d-flex align-items-center justify-content-center">
            <img alt="" class="mw-100 mh-100" src="/media/${data}">
        </div>`
}
// Function to format columns
function formatColumns(columns) {
    //console.log("typeof columns: ", typeof columns)
    return columns.map(column => {
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

