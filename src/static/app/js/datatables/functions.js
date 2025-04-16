

async function fetchData(url) {
    var columns = [];

    await fetch(ajaxUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Initial data:', data.data);
            indexes1 = data.indexes
            columns = data.columns;

            //columns1[0].class = 'btn btn-outline-theme text-success'
        })
        .catch(error => {
            console.error('Error initializing table:', error);
            alert('Failed to initialize table. Please check the server connection.');
        });

    return columns
}


function getImage(data, row) {
    return `
        <div class="d-flex align-items-center" id="row-image">
            <div class="w-50px h-50px bg-inverse bg-opacity-25 d-flex align-items-center justify-content-center">
                <img alt="" class="mw-100 mh-100" src="/media/${data}">
            </div>
            <div class="ms-3">
                <a href="#" 
                    class="text-inverse text-opacity-75 text-decoration-none"
                    hx-on::click="alert(row.name)"
                    >${row.name}</a>
            </div>
        </div>`
}

function getCode(data, row) {
    var codeData;
    if (row.code) {
        codeData = row.code
    } else if (row.number) {
        codeData = row.number
    } else {
        codeData = row.id
    }
    return `
        <div class="form-check d-flex align-items-center h-50px">
            <input type="checkbox" class="form-check-input me-3" id="${data}">
            <label class="form-check-label" for="${data}">${codeData}</label>
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
                <a href="#" 
                    class="text-inverse text-opacity-75 text-decoration-none">${data}</a>
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

function getActions(data, row) {
    var id = row.id ? row.id : row.number;

    return `
        <div class="btn-group btn-group-md">
            <button type="button" class="btn" 
                hx-get="/pos/modal-product/${id}/" 
                hx-target="#modalPosItem" hx-trigger="click" 
                data-bs-target="#modalPosItem" 
                data-bs-toggle="modal"
                >
                <i class="fas fa-md fa-fw me-1 fa-edit"></i>
            </button>
            <button type="button" class="btn" hx-delete="/pos/delete-order-item/${id}/" hx-target="#calculations-sales-06122024-3773" hx-swap="innerHTML" hx-on:delete-order-item="htmx.find('#order-item-1-31032025-01-3904').remove()" hx-on::before-request="htmx.find('#order-item-1-31032025-01-3904').classList.add('d-none');
                console.log(event.detail.successful)
            " hx-on::after-request="
            htmx.find('#order-${id}').classList.remove('d-none');
            if (!event.detail.successful) {
                console.log(event.detail.successful)
                const errorSpan = document.createElement('span');
                console.log(errorSpan)
                errorSpan.textContent = 'Failed to remove item!';
                errorSpan.classList.add('text-danger');
                htmx.find('#order-${id}').appendChild(errorSpan);
            }
            ">
                <i class="fas fa-md fa-fw me-1 fa-trash text-danger"></i>
            </button>
        </div>
        `
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