//selectElementIds = select elements
//dataSource = data source from json file in static
//dataUrl = data source from url query
//queryBy = query the bloodhound by
//displayValueKeys = values to be displayed in the option tag
//valueKeys = values to be set in option value tag
//subtextKeys = values to be set as subtext

function setupSelectData(selectElementIds, dataSource, dataUrl, queryBy, displayValueKeys, valueKeys, subtextKeys) {
  //Dont run if the element is not on page
  if($('#'+selectElementIds[0]).length == 0) {
    return
  }
  if(dataUrl) {
    $('.bs-searchbox').append(`
    <div id="input-spinner" class="hide form-control-spinner spinner-border spinner-border-sm text-primary" role="status">
      <span class="sr-only">Loading...</span>
    </div>
    `)
  }
  function makeBloodHound() {
    if(queryBy != null) {
      datumTokenizer = Bloodhound.tokenizers.obj.whitespace(queryBy)
    } else {
      datumTokenizer = Bloodhound.tokenizers.whitespace
    }
    
    if(dataUrl) {
      return new Bloodhound({
        datumTokenizer: datumTokenizer,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
          url: dataUrl+'%QUERY',
          wildcard: '%QUERY'
        }
      });
    } else if (dataSource) {
      return new Bloodhound({
        datumTokenizer: datumTokenizer,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
          url: '/static/'+dataSource+'.json',
          cache: false,
        },
      }); 
    }
  }
  function getInputField(id) {
    const ownerId = $('[data-id='+id+']').attr('aria-owns') //a button
    return $('[aria-controls='+ownerId+']') //an input (owned by the button)
  }
  function makeValueFromKeys(data, keys) {
    value = ''
    keys.forEach(key => {
      value += data[key] + ' '
    })
    return value.trim()
  }
  function makeOptionElement(result) {
    if(displayValueKeys != null ) {
      displayValue = makeValueFromKeys(result, displayValueKeys)
    } else {
      displayValue = result
    }
    var option = new Option(displayValue)
    option.setAttribute("data-tokens", displayValue);
    if(subtextKeys != null ) {
      subtext = makeValueFromKeys(result, subtextKeys)
      option.setAttribute("data-subtext", subtext);
    }
    if(valueKeys != null ) {
      value = makeValueFromKeys(result, valueKeys)
      option.setAttribute("value", value);
    }
    return option
  }
  function responseSyncORAsync(element, results) { 
    element.empty()
    results.forEach(result => {
      element.append(makeOptionElement(result));
    }); 
    element.selectpicker('refresh');
    $('#input-spinner').hide()
  }
  function listenAndUpdateData(elementId, query) {
    const selectElement = $('#'+elementId)
    bloodhound.search(query, function(datums) {
      //File data results are sync
      if(dataSource) {
        responseSyncORAsync(selectElement, datums)
      }
    }, function(datums) {
      //Remote url data results are async
      if(dataUrl) {
        responseSyncORAsync(selectElement, datums)
      }
    }) 
  }
  const bloodhound = makeBloodHound()
  selectElementIds.forEach(elementId => {
    const selectInput = getInputField(elementId)
    selectInput.on('input', function() {
      if(this.value.length == 0) {
        const selectElement = $('#'+elementId)
        selectElement.empty()
        selectElement.selectpicker('refresh');
        return;
      }
      if(this.value.length > 0) {
        $('#input-spinner').show()
        listenAndUpdateData(elementId, this.value)
      }
    });
  })
}
