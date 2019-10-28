
function setupSelectFieldData(selectElementIds, dataSource, dataKeys, queryBy) {
  //Dont run if the element is not on page
  if($('#'+selectElementIds[0]).length == 0) {
    return
  }
  function makeBloodHound() {
    if(queryBy != null) {
      datumTokenizer = Bloodhound.tokenizers.obj.whitespace(queryBy)
    } else {
      datumTokenizer = Bloodhound.tokenizers.whitespace
    }
    return new Bloodhound({
      datumTokenizer: datumTokenizer,
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: {
        url: '/static/'+dataSource+'.json',
        cache: false,
      },
    }); 
  }
  function getInputField(id) {
    const ownerId = $('[data-id='+id+']').attr('aria-owns') //a button
    return $('[aria-controls='+ownerId+']') //an input (owned by the button)
  }
  function makeOptionElement(result) {
    if(dataKeys != null ) {
      value = ''
      dataKeys.forEach(key => {
        value += result[key] + ' '
      })
    } else {
      value = result
    }
    var option = new Option(value)
    option.setAttribute("data-tokens",value);
    return option
  }
  function listenAndUpdateData(elementId, query) {
    const selectElement = $('#'+elementId)
    bloodhound.search(query , function(results) {
      selectElement.empty()
      results.forEach(result => {
        selectElement.append(makeOptionElement(result));
      }); 
      selectElement.selectpicker('refresh');
    });
  }
  const bloodhound = makeBloodHound()
  selectElementIds.forEach(elementId => {
    const selectInput = getInputField(elementId)
    selectInput.on('keyup',function(){
      if(this.value.length > 1) {
        listenAndUpdateData(elementId, this.value)
      }
    })
  })
}


function setupSelectRemoteData(selectElementIds, dataSource, dataKeys, queryBy) {
  //Dont run if the element is not on page
  if($('#'+selectElementIds[0]).length == 0) {
    return
  }
  $('.bs-searchbox').append(`
  <div id="input-spinner" class="hide form-control-spinner spinner-border spinner-border-sm text-primary" role="status">
    <span class="sr-only">Loading...</span>
  </div>
  `)
  function makeBloodHound() {
    if(queryBy != null) {
      datumTokenizer = Bloodhound.tokenizers.obj.whitespace('name')
    } else {
      datumTokenizer = Bloodhound.tokenizers.whitespace
    }
    return new Bloodhound({
      datumTokenizer: datumTokenizer,
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      remote: {
        url: '/kaucu/contact/search/%QUERY',
        wildcard: '%QUERY'
      }
    }); 
  }
  function getInputField(id) {
    const ownerId = $('[data-id='+id+']').attr('aria-owns') //a button
    return $('[aria-controls='+ownerId+']') //an input (owned by the button)
  }
  function makeOptionElement(result) {
    if(dataKeys != null ) {
      value = ''
      dataKeys.forEach(key => {
        value += result[key] + ' '
      })
    } else {
      value = result
    }
    var option = new Option(value)
    option.setAttribute("data-tokens",value);
    option.setAttribute("value", result['id']);
    option.setAttribute("data-subtext", result['slug']);

    console.log(option)
    return option
  }
  function sync(datums) { }


  function listenAndUpdateData(elementId, query) {
    const selectElement = $('#'+elementId)
    bloodhound.search(query, sync, function(results) {
      selectElement.empty()
      results.forEach(result => {
        selectElement.append(makeOptionElement(result));
      }); 
      selectElement.selectpicker('refresh');
      $('#input-spinner').hide()
    });
  }
  const bloodhound = makeBloodHound()


  selectElementIds.forEach(elementId => {
    const selectInput = getInputField(elementId)
    selectInput.on('keyup',function(){
      if(this.value.length > 1) {
        $('#input-spinner').show()
        listenAndUpdateData(elementId, this.value)
      }
    }) 
  })
}
