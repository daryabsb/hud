var renderDataTable = function (elId, options = {}) {

    var options = {
        //dom: "-sm-12 col-md-5 fs-12px'i><'col-sm-12 col-md-7 fs-12px'p>>",
        ...options,

    }
    new DataTable(`#${elId}`, options);
};