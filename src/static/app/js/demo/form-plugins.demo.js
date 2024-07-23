var handleRenderDatepicker = function () {
    $('#datepicker-default').datepicker({ autoclose: true });
    $('#datepicker-component').datepicker({ autoclose: true });
    $('#datepicker-range').datepicker({ autoclose: true });
    $('#datepicker-inline').datepicker({ autoclose: true });
};
var handleDateRangePicker = function () {
    $('#default-daterange').daterangepicker({
        opens: 'right', format: 'MM/DD/YYYY',
        separator: ' to ', startDate: moment().subtract(29, 'days'),
        endDate: moment(), minDate: '01/01/2012', maxDate: '12/31/2018',
    },
        function (start, end) {
            $('#default-daterange input').val(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        });
    $('#advance-daterange span').html(moment().subtract('days', 29).format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));
    $('#advance-daterange').daterangepicker({
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
var handleRenderTimepicker = function () {
    $('#timepicker-default').timepicker();
    $('#timepicker-seconds').timepicker({
        minuteStep: 1, appendWidgetTo: 'body',
        showSeconds: true, showMeridian: false,
        defaultTime: false, template: false
    });
};
var handleRenderColorpicker = function () {
    $('#colorpicker-default').spectrum({ showInput: true });
    $('#colorpicker-component').spectrum({ showInput: true });
};
var handleRenderTypeahead = function () {
    $.typeahead({
        input: '#typeahead',
        order: "desc", source: {
            data: [
                "Australia", "France", "Iran", "Iraq", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia"
            ]
        }
    });
};
var handleRenderTagsInput = function () {
    var elt = '#jquery-tagit';
    $(elt).tagit({
        fieldName: 'tags',
        availableTags: ['c++', 'java', 'php', 'javascript', 'ruby', 'python', 'c'],
        autocomplete: {
            delay: 0,
            minLength: 2
        }
    });
};
var handleRenderBootstrapSlider = function () {
    $('#slider-default').bootstrapSlider();
    $('#slider-range').bootstrapSlider();
    $('#slider-tooltip').bootstrapSlider({
        tooltip: 'always'
    });
    $('#slider-vertical').bootstrapSlider({
        reversed: true
    });
    $('#slider-disabled').bootstrapSlider();
};
var handleRenderMaskedInput = function () {
    $('#masked-input-date').mask('99/99/9999');
    $('#masked-input-phone').mask('(999) 999-9999');
};
var handleRenderSummernote = function () {
    $('.summernote').summernote({ height: 300 });
};

var handleRenderjQueryFileUpload = function () {
    $('#fileupload').fileupload({
        previewMaxHeight: 80,
        previewMaxWidth: 120,
        url: '//jquery-file-upload.appspot.com/',
        disableImageResize: /Android(?!.*Chrome)|Opera/.test(window.navigator.userAgent),
        maxFileSize: 999000, acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i
    });
    $('#fileupload').on('fileuploadchange', function (e, data) {
        $('#fileupload .empty-row').hide();
    });
    $('#fileupload').on('fileuploadfail',
        function (e, data) {
            if (data.errorThrown === 'abort') {
                if ($('#fileupload .files tr').not('.empty-row').length == 1) {
                    $('#fileupload .empty-row').show();
                }
            }
        });

    if ($.support.cors) {
        $.ajax({ url: '//jquery-file-upload.appspot.com/', type: 'HEAD' }).fail(function () {
            var alert = '<div class="alert alert-danger m-b-0 m-t-15">Upload server currently unavailable - ' + new Date() + '</div>'; $('#fileupload #error-msg').removeClass('d-none').html(alert);
        });
    }
};

var handleRenderSelectPicker = function () {
    $('#ex-basic').picker();
    $('#ex-multiselect').picker();
    $('#ex-search').picker({ search: true });
};

$(document).ready(function () {
    handleRenderDatepicker();
    handleDateRangePicker();
    handleRenderTimepicker();
    handleRenderColorpicker();
    handleRenderTypeahead();
    handleRenderTagsInput();
    handleRenderBootstrapSlider();
    handleRenderMaskedInput();
    handleRenderSummernote();
    handleRenderjQueryFileUpload();
    handleRenderSelectPicker();
});