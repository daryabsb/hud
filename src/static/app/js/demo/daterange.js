var handleDateRangePicker = function () {
    // $('#default-daterange').daterangepicker({
    //     opens: 'right', format: 'MM/DD/YYYY',
    //     separator: ' to ', startDate: moment().subtract(29, 'days'),
    //     endDate: moment(), minDate: '01/01/2012', maxDate: '12/31/2018',
    // },
    //     function (start, end) {
    //         $('#default-daterange input').val(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    //     });
    // $('#advance-daterange span').html(moment().subtract('days', 29).format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));
    $('#datepicker').daterangepicker({
        format: 'MM/DD/YYYY', startDate: moment().subtract(29, 'days'),
        endDate: moment(), minDate: '01/01/2012', maxDate: '12/31/2015',
        dateLimit: { days: 60 }, showDropdowns: true, showWeekNumbers: true, timePicker: false,
        timePickerIncrement: 1, timePicker12Hour: true, ranges: {
            'Today': [moment(), moment()], 'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()], 'Last 30 Days': [moment().subtract(29, 'days'),
            moment()
            ],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'),
            moment().subtract(1, 'month').endOf('month')]
        },
        opens: 'right', drops: 'down', buttonClasses: ['btn', 'btn-sm'],
        applyClass: 'btn-primary', cancelClass: 'btn-default', separator: ' to ',
        locale: {
            applyLabel: 'Submit', cancelLabel: 'Cancel', fromLabel: 'From', toLabel: 'To',
            customRangeLabel: 'Custom', daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
            monthNames: [
                'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                'September', 'October', 'November', 'December'], firstDay: 1
        }
    }, function (start, end, label) {
        $('#advance-daterange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    });
};
document.addEventListener('DOMContentLoaded', function () {

    // handleRenderDatepicker();
    // handleDateRangePicker();
    // handleRenderTimepicker();
    // handleRenderColorpicker();
    // handleRenderTypeahead();
    // handleRenderTagsInput();
    // handleRenderBootstrapSlider();
    // handleRenderMaskedInput();
    // handleRenderSummernote();
    // handleRenderjQueryFileUpload();
    // handleRenderSelectPicker();
    $('#daterange').daterangepicker({
        opens: 'right',
        format: 'MM/DD/YYYY',
        separator: ' to ',
        startDate: moment().subtract('days', 29),
        endDate: moment(),
        minDate: '01/01/2012',
        maxDate: '12/31/2018',
    }, function (start, end) {
        $('#daterange input').val(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    });
});