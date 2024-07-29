var renderDataTable = function (elId) {
    var header = document.getElementById('header')
    var height = window.innerHeight - header.offsetHeight - 25;
    var width = window.innerWidth;

    var options = {
        //dom: "-sm-12 col-md-5 fs-12px'i><'col-sm-12 col-md-7 fs-12px'p>>",
        scrollX: width - 100,
        pageLength: 20,
        lengthMenu: [10, 20, 50, 75, 100],
        //scrollX: true,
        //scrollY: 500,
        //scrollY: height,
        //scroller: true,
        //responsive: true,
        //deferRender:    true,
        autoWidth: true,
        select: true,
        fixedHeader: true,
        fixedColumns: { left: 3 },
        order: [[1, 'asc']],

    }
    var table = new DataTable(`#${elId}`, options);
};

var handleDataTable = function () {
    var header = document.getElementById('header')
    var height = window.innerHeight - header.offsetHeight - 25;
    var width = window.innerWidth;

    var options = {
        //dom: "-sm-12 col-md-5 fs-12px'i><'col-sm-12 col-md-7 fs-12px'p>>",
        scrollX: width - 100,
        pageLength: 20,
        lengthMenu: [10, 20, 50, 75, 100],
        //scrollX: true,
        //scrollY: 500,
        scrollY: height,
        //scroller: true,
        //responsive: true,
        //deferRender:    true,
        autoWidth: true,
        select: true,
        fixedHeader: true,
        fixedColumns: { left: 3 },
        order: [[1, 'asc']],

        //order: [[1, 'asc']],
        //columnDefs: [{ targets: 'no-sort', orderable: false }],
        /*
        columns: [
            { "data": "number" },
            { "data": "cash_register" },
            { "data": "date", "render": function(data) {
                return new Date(data).toLocaleString();
            }},
            { "data": "reference_document_number" },
            { "data": "due_date", "render": function(data) {
                return new Date(data).toLocaleString();
            }},
            { "data": "paid_status", "render": function(data) {
                return data ? 'Paid' : 'Unpaid';
            }}
        ] 
        
        */
    }

    var table = new DataTable('#documents-table', options);
    console.log(table)
};
