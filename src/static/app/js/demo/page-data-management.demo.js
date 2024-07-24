var handleRenderTableData = function () {
    var height = $(window).height() - $('#header').height() - 165;
    var options = {
        dom: "-sm-12 col-md-5 fs-12px'i><'col-sm-12 col-md-7 fs-12px'p>>",
        scrollY: height,
        scrollX: true,
        paging: false,
        fixedColumns: { left: 3 },
        order: [[1, 'asc']],
        columnDefs: [{ targets: 'no-sort', orderable: false }],
        buttons: [{
            extend: 'excel', text: '<i class="fa fa-download fa-fw me-1"></i> Export Excel',
            className: 'btn btn-outline-default btn-sm text-nowrap rounded-2', footer: true
        }]
    };
    if ($(window).width() < 767) { options.fixedColumns = { left: 2 }; }
    $('#datatable').DataTable(options); $('[data-id="table"]').removeClass('d-none'); handelTooltipPopoverActivation(); $(window).trigger('resize');
}; $(document).ready(function () { handleRenderTableData(); });