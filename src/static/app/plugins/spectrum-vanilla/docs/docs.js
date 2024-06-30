import Spectrum from '../dist/spectrum.es.js';

function updateBorders(color) {
  // do nothing
}

$(function () {

  $('pre').each(function () {
    hljs.highlightBlock(this);
  });

  $('#toc').toc({
    'selectors': 'h1,h2:not(.subtitle),h3', //elements to use as headings
    'container': '.main-container', //element to find all selectors in
    'smoothScrolling': true, //enable or disable smooth scrolling on click
    'prefix': 'toc', //prefix for anchor tags and class names
    'highlightOnScroll': true, //add class to heading that is currently in focus
    'highlightOffset': 100, //offset to trigger the next headline
    'anchorName': function (i, heading, prefix) { //custom function for anchor name
      return heading.id || prefix + i;
    }
  });

// ----- CONFIGURATOR -----
  var spInstance = Spectrum.getInstance('#color-picker');

  initConfigurator();
  updateColorPickerAndJavascriptCode();

  $('.configurator-container').find('input[type=radio], input[type=checkbox]').on('click', function () {
    updateColorPickerAndJavascriptCode();
  });

  function initConfigurator() {
    $('.configurator-container input[type=checkbox]').each(function () {
      var value = spInstance.option($(this).data('rule'));
      $(this).prop('checked', value);
    });

    const type = spInstance.option('type');
    $('.configurator-container input[name=type]').val([ type ]);
  }

  function updateColorPickerAndJavascriptCode() {
    spInstance.off();
    spInstance.on('change', function () {
      document.documentElement.style.setProperty('--primary-color', $(this).val());
    });
    var options = {
      type: $('.configurator-container input[name=type]:checked').val()
    };
    $('.configurator-container input[type=checkbox]').each(function () {
      var optionName = $(this).data('rule');
      var value = $(this).is('[type=checkbox]') ? $(this).is(':checked') : $(this).val();
      options[optionName] = value;
    });

    var javascriptCode = 'const sp = Spectrum::getInstance(\'#color-picker\', {';
    var optionsCount = 0;
    for (var i in options) {
      if (options[i] != $.fn.spectrum.defaults[i]) {
        optionsCount++;
        var val = options[i];
        if (typeof val === 'string' && val != 'true' && val != 'false') val = '"' + options[i] + '"';
        javascriptCode += '\n  ' + i + ': ' + val + ',';
      }
    }
    if (optionsCount > 0) {
      javascriptCode = javascriptCode.slice(0, -1); // remove last ",\n"
      javascriptCode += '\n';
    }
    javascriptCode += '});';
    $('pre#sp-options').html(javascriptCode);
    hljs.highlightBlock($('pre#sp-options')[0]);

    spInstance.rebuild(options);
  }

// ----- END CONFIGURATOR -----

  Spectrum.getInstance('#hideButtons', {
    showButtons: false,
    change: updateBorders
  });

  var isDisabled = true;
  $('#toggle-disabled').on('click', function () {
    if (isDisabled) {
      $('#disabled').spectrum('enable');
    } else {
      $('#disabled').spectrum('disable');
    }
    isDisabled = !isDisabled;
    return false;
  });

  Spectrum.getInstance('input:disabled', {});
  Spectrum.getInstance('#disabled', {
    disabled: true
  });

  // Spectrum.getInstance('#pick1', {
  //   flat: true,
  //   change: function (color) {
  //     var hsv = color.toHsv();
  //     var rgb = color.toRgbString();
  //     var hex = color.toHexString();
  //     //console.log("callback",color.toHslString(), color.toHsl().h, color.toHsl().s, color.toHsl().l)
  //     $('#docs-content').css({
  //       'background-color': color.toRgbString()
  //     }).toggleClass('dark', hsv.v < .5);
  //     $('#switch-current-rgb').text(rgb);
  //     $('#switch-current-hex').text(hex);
  //   },
  //   show: function () {
  //
  //   },
  //   hide: function () {
  //
  //   },
  //   showInput: true,
  //   showPalette: true,
  //   palette: [ 'white', '#306', '#c5c88d', '#ac5c5c', '#344660' ]
  // });

  // Spectrum.getInstance('#collapsed', {
  //   color: '#dd3333',
  //   change: updateBorders,
  //   show: function () {
  //
  //   },
  //   hide: function () {
  //
  //   }
  // });

  // Spectrum.getInstance('#flat', {
  //   flat: true,
  //   showInput: true,
  //   move: updateBorders
  // });
  //
  // Spectrum.getInstance('#flatClearable', {
  //   flat: true,
  //   move: updateBorders,
  //   change: updateBorders,
  //   allowEmpty: true,
  //   showInput: true
  // });

  Spectrum.getInstance('#showInput', {
    color: '#dd33dd',
    showInput: true,
    change: updateBorders,
    show: function () {

    },
    hide: function () {

    }
  });

  Spectrum.getInstance('#showAlpha', {
    color: 'rgba(255, 128, 0, .5)',
    showAlpha: true,
    change: updateBorders
  });

  Spectrum.getInstance('#showAlphaWithInput', {
    color: 'rgba(255, 128, 0, .5)',
    showAlpha: true,
    showInput: true,
    showPalette: true,
    palette: [
      [ 'rgba(255, 128, 0, .9)', 'rgba(255, 128, 0, .5)' ],
      [ 'red', 'green', 'blue' ],
      [ 'hsla(25, 50, 75, .5)', 'rgba(100, .5, .5, .8)' ]
    ],
    change: updateBorders
  });

  // Spectrum.getInstance('#showAlphaWithInputAndEmpty', {
  //   color: 'rgba(255, 128, 0, .5)',
  //   allowEmpty: true,
  //   showAlpha: true,
  //   showInput: true,
  //   showPalette: true,
  //   palette: [
  //     [ 'rgba(255, 128, 0, .9)', 'rgba(255, 128, 0, .5)' ],
  //     [ 'red', 'green', 'blue' ],
  //     [ 'hsla(25, 50, 75, .5)', 'rgba(100, .5, .5, .8)' ]
  //   ],
  //   change: updateBorders
  // });

  Spectrum.getInstance('#showInputWithClear', {
    allowEmpty: true,
    color: '',
    showInput: true,
    change: updateBorders,
    show: function () {

    },
    hide: function () {

    }
  });

  Spectrum.getInstance('#openWithLink', {
    color: '#dd3333',
    change: updateBorders,
    show: function () {

    },
    hide: function () {

    }
  });

  // Spectrum.getInstance('#className', {
  //   className: 'awesome'
  // });

  Spectrum.getInstance('#replacerClassName', {
    replacerClassName: 'awesome',
    allowEmpty: true,
    color: ''
  });

  Spectrum.getInstance('#containerClassName', {
    containerClassName: 'awesome'
  });

  Spectrum.getInstance('#showPalette', {
    showPalette: true,
    palette: [
      [ 'black', 'white', 'blanchedalmond' ],
      [ 'rgb(255, 128, 0);', 'hsv 100 70 50', 'lightyellow' ]
    ],
    hide: function (e) {
      var c = e.detail.color;
      var label = $('[data-label-for=' + this.id + ']');
      label.text('Hidden: ' + c.toHexString());
    },
    change: function (e) {
      var c = e.detail.color;
      var label = $('[data-label-for=' + this.id + ']');
      label.text('Change called: ' + c.toHexString());
    },
    move: function (e) {
      var c = e.detail.color;
      var label = $('[data-label-for=' + this.id + ']');
      label.text('Move called: ' + c.toHexString());
    }
  });

  var textPalette = [ 'rgb(255, 255, 255)', 'rgb(204, 204, 204)', 'rgb(192, 192, 192)', 'rgb(153, 153, 153)', 'rgb(102, 102, 102)', 'rgb(51, 51, 51)', 'rgb(0, 0, 0)', 'rgb(255, 204, 204)', 'rgb(255, 102, 102)', 'rgb(255, 0, 0)', 'rgb(204, 0, 0)', 'rgb(153, 0, 0)', 'rgb(102, 0, 0)', 'rgb(51, 0, 0)', 'rgb(255, 204, 153)', 'rgb(255, 153, 102)', 'rgb(255, 153, 0)', 'rgb(255, 102, 0)', 'rgb(204, 102, 0)', 'rgb(153, 51, 0)', 'rgb(102, 51, 0)', 'rgb(255, 255, 153)', 'rgb(255, 255, 102)', 'rgb(255, 204, 102)', 'rgb(255, 204, 51)', 'rgb(204, 153, 51)', 'rgb(153, 102, 51)', 'rgb(102, 51, 51)', 'rgb(255, 255, 204)', 'rgb(255, 255, 51)', 'rgb(255, 255, 0)', 'rgb(255, 204, 0)', 'rgb(153, 153, 0)', 'rgb(102, 102, 0)', 'rgb(51, 51, 0)', 'rgb(153, 255, 153)', 'rgb(102, 255, 153)', 'rgb(51, 255, 51)', 'rgb(51, 204, 0)', 'rgb(0, 153, 0)', 'rgb(0, 102, 0)', 'rgb(0, 51, 0)', 'rgb(153, 255, 255)', 'rgb(51, 255, 255)', 'rgb(102, 204, 204)', 'rgb(0, 204, 204)', 'rgb(51, 153, 153)', 'rgb(51, 102, 102)', 'rgb(0, 51, 51)', 'rgb(204, 255, 255)', 'rgb(102, 255, 255)', 'rgb(51, 204, 255)', 'rgb(51, 102, 255)', 'rgb(51, 51, 255)', 'rgb(0, 0, 153)', 'rgb(0, 0, 102)', 'rgb(204, 204, 255)', 'rgb(153, 153, 255)', 'rgb(102, 102, 204)', 'rgb(102, 51, 255)', 'rgb(102, 0, 204)', 'rgb(51, 51, 153)', 'rgb(51, 0, 153)', 'rgb(255, 204, 255)', 'rgb(255, 153, 255)', 'rgb(204, 102, 204)', 'rgb(204, 51, 204)', 'rgb(153, 51, 153)', 'rgb(102, 51, 102)', 'rgb(51, 0, 51)' ];

  Spectrum.getInstance('#showPaletteOnly', {
    color: 'blanchedalmond',
    showPaletteOnly: true,
    showPalette: true,
    palette: [
      [ 'black', 'white', 'blanchedalmond',
        'rgb(255, 128, 0);', 'hsv 100 70 50' ],
      [ 'red', 'yellow', 'green', 'blue', 'violet' ]
    ],
    change: function (e) {
      var c = e.detail.color;
      var label = $('[data-label-for=' + this.id + ']');
      label.text('Change called: ' + c.toHexString());
    },
    move: function (e) {
      var c = e.detail.color;
      var label = $('[data-label-for=' + this.id + ']');
      label.text('Move called: ' + c.toHexString());
    }
  });

  Spectrum.getInstance('#hideAfterPaletteSelect', {
    showPaletteOnly: true,
    showPalette: true,
    hideAfterPaletteSelect: true,
    color: 'blanchedalmond',
    palette: [
      [ 'black', 'white', 'blanchedalmond',
        'rgb(255, 128, 0);', 'hsv 100 70 50' ],
      [ 'red', 'yellow', 'green', 'blue', 'violet' ]
    ],
    change: function (e) {
      var c = e.detail.color;
      var label = $('[data-label-for=' + this.id + ']');
      label.text('Change called: ' + c.toHexString());
    },
    move: function (e) {
      var c = e.detail.color;
      var label = $('[data-label-for=' + this.id + ']');
      label.text('Move called: ' + c.toHexString());
    }
  });

  Spectrum.getInstance('#togglePaletteOnly', {
    color: 'blanchedalmond',
    showPaletteOnly: true,
    togglePaletteOnly: true,
    showPalette: true,
    palette: [
      [ '#000', '#444', '#666', '#999', '#ccc', '#eee', '#f3f3f3', '#fff' ],
      [ '#f00', '#f90', '#ff0', '#0f0', '#0ff', '#00f', '#90f', '#f0f' ],
      [ '#f4cccc', '#fce5cd', '#fff2cc', '#d9ead3', '#d0e0e3', '#cfe2f3', '#d9d2e9', '#ead1dc' ],
      [ '#ea9999', '#f9cb9c', '#ffe599', '#b6d7a8', '#a2c4c9', '#9fc5e8', '#b4a7d6', '#d5a6bd' ],
      [ '#e06666', '#f6b26b', '#ffd966', '#93c47d', '#76a5af', '#6fa8dc', '#8e7cc3', '#c27ba0' ],
      [ '#c00', '#e69138', '#f1c232', '#6aa84f', '#45818e', '#3d85c6', '#674ea7', '#a64d79' ],
      [ '#900', '#b45f06', '#bf9000', '#38761d', '#134f5c', '#0b5394', '#351c75', '#741b47' ],
      [ '#600', '#783f04', '#7f6000', '#274e13', '#0c343d', '#073763', '#20124d', '#4c1130' ]
    ]
  });

  Spectrum.getInstance('#clickoutFiresChange', {
    change: updateBorders
  });

  Spectrum.getInstance('#clickoutDoesntFireChange', {
    change: updateBorders,
    clickoutFiresChange: false
  });

  Spectrum.getInstance('#showInitial', {
    showInitial: true
  });

  Spectrum.getInstance('#showInputAndInitial', {
    showInitial: true,
    showInput: true
  });

  Spectrum.getInstance('#showInputInitialClear', {
    allowEmpty: true,
    showInitial: true,
    showInput: true
  });

  Spectrum.getInstance('#changeOnMove', {
    move: function (e) {
      var c = e.detail.color;
      var label = $('[data-label-for=' + this.id + ']');
      label.text('Move called: ' + c.toHexString());
    }
  });
  Spectrum.getInstance('#changeOnMoveNo', {
    showInput: true,
    change: function (e) {
      var c = e.detail.color;
      var label = $('[data-label-for=' + this.id + ']');
      label.text('Change called: ' + c.toHexString());
    }
  });

  function prettyTime() {
    var date = new Date();

    return date.toLocaleTimeString();
  }

  Spectrum.getInstance('#eventshow', {
    show: function (e) {
      var c = e.detail.color;
      var label = $('#eventshowLabel');
      label.text('show called at ' + prettyTime() + ' (color is ' + c.toHexString() + ')');
    }
  });

  Spectrum.getInstance('#eventhide', {
    hide: function (e) {
      var c = e.detail.color;
      var label = $('#eventhideLabel');
      label.text('hide called at ' + prettyTime() + ' (color is ' + c.toHexString() + ')');
    }
  });

  Spectrum.getInstance('#eventdragstart', {
    showAlpha: true
  }).on('dragstart', function (e) {
    var c = e.detail.color;
    var label = $('#eventdragstartLabel');
    label.text('dragstart called at ' + prettyTime() + ' (color is ' + c.toHexString() + ')');
  });

  Spectrum.getInstance('#eventdragstop', {
    showAlpha: true
  }).on('dragstop', function (e) {
    var c = e.detail.color;
    var label = $('#eventdragstopLabel');
    label.text('dragstop called at ' + prettyTime() + ' (color is ' + c.toHexString() + ')');
  });

  Spectrum.getInstanceMultiple('.basic', { change: updateBorders });
  Spectrum.getInstanceMultiple('.override', {
    color: 'yellow',
    change: updateBorders
  });

  Spectrum.getInstanceMultiple('.startEmpty', {
    allowEmpty: true,
    change: updateBorders
  });

  Spectrum.getInstance('#beforeShow', {
    beforeShow: function () {
      return false;
    }
  });

  // Spectrum.getInstance('#custom', {
  //   color: '#f00'
  // });

  Spectrum.getInstance('#buttonText', {
    locale: 'fr',
    chooseText: 'OK!'
  });

  Spectrum.getInstance('#showSelectionPalette', {
    showPalette: true,
    showSelectionPalette: true, // true by default
    palette: []
  });
  Spectrum.getInstance('#showSelectionPaletteStorage', {
    showPalette: true,
    localStorageKey: 'spectrum.homepage', // Any picker with the same string will share selection
    showSelectionPalette: true,
    palette: []
  });
  Spectrum.getInstance('#showSelectionPaletteStorage2', {
    showPalette: true,
    localStorageKey: 'spectrum.homepage', // Any picker with the same string will share selection
    showSelectionPalette: true,
    palette: []
  });

  Spectrum.getInstance('#selectionPalette', {
    showPalette: true,
    palette: [],
    showSelectionPalette: true, // true by default
    selectionPalette: [ 'red', 'green', 'blue' ]
  });

  Spectrum.getInstance('#maxSelectionSize', {
    showPalette: true,
    palette: [],
    showSelectionPalette: true, // true by default
    selectionPalette: [ 'red', 'green', 'blue' ],
    maxSelectionSize: 2
  });

  Spectrum.getInstance('#preferredHex', {
    preferredFormat: 'hex',
    showInput: true,
    showPalette: true,
    palette: [ [ 'red', 'rgba(0, 255, 0, .5)', 'rgb(0, 0, 255)' ] ]
  });
  Spectrum.getInstance('#preferredHex3', {
    preferredFormat: 'hex3',
    showInput: true,
    showPalette: true,
    palette: [ [ 'red', 'rgba(0, 255, 0, .5)', 'rgb(0, 0, 255)' ] ]
  });
  Spectrum.getInstance('#preferredHsl', {
    preferredFormat: 'hsl',
    showInput: true,
    showPalette: true,
    palette: [ [ 'red', 'rgba(0, 255, 0, .5)', 'rgb(0, 0, 255)' ] ]
  });
  Spectrum.getInstance('#preferredRgb', {
    preferredFormat: 'rgb',
    showInput: true,
    showPalette: true,
    palette: [ [ 'red', 'rgba(0, 255, 0, .5)', 'rgb(0, 0, 255)' ] ]
  });
  Spectrum.getInstance('#preferredName', {
    preferredFormat: 'name',
    showInput: true,
    showPalette: true,
    palette: [ [ 'red', 'rgba(0, 255, 0, .5)', 'rgb(0, 0, 255)' ] ]
  });
  Spectrum.getInstance('#preferredNone', {
    showInput: true,
    showPalette: true,
    palette: [ [ 'red', 'rgba(0, 255, 0, .5)', 'rgb(0, 0, 255)' ] ]
  });

  const triggerSet = Spectrum.getInstance('#triggerSet', {
    change: updateBorders
  });

  // Show the original input to demonstrate the value changing when calling `set`
  triggerSet.show();

  const input = document.querySelector('#enterAColor');
  document.querySelector('#btnEnterAColor').addEventListener('click', () => {
    triggerSet.set(input.value);
  });

  $('#toggle').spectrum();
  $('#btn-toggle').on('click', function () {
    $('#toggle').spectrum('toggle');
    return false;
  });

});
