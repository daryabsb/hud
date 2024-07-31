console.log(productListUrl);
var width = window.innerWidth;
document.addEventListener('DOMContentLoaded', function () {
    var table = document.getElementById('products-table');
    fetch(productListUrl)
        .then(response => response.json())
        .then(data => {
            var formattedColumns = formatColumns(data.columns);
            let toolbar = document.createElement('div');
            toolbar.innerHTML = topToolbar // '<b>Custom tool bar! Text/images etc.</b>';
            new DataTable(table, {
                ordering: false,
                ajax: {
                    url: productListUrl,
                    dataSrc: 'data',
                },
                scrollX: width - 335,
                processing: true,
                columns: formattedColumns,
                serverSide: true,
                select: true,
                layout: {
                    top: toolbar
                }
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
// Function to format columns
function formatColumns(columns) {
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

        if (column.data === 'is_tax_inclusive_price' || column.data === 'is_enabled' || column.data === 'is_price_change_allowed' || column.data === 'is_service') {
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