function ProctoringHideXBlock(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
  
    $(element).find('.save-button').bind('click', function(e) {
      var form_data = new FormData();
      var display_name = $(element).find('input[name=display_name]').val();
      form_data.append('display_name', display_name);
      runtime.notify('save', {state: 'start'});
  
      $.ajax({
        url: handlerUrl,
        dataType: 'text',
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,
        type: "POST",
        success: function(response){
          runtime.notify('save', {state: 'end'});
        }
      });
      e.preventDefault();
  
    });
  
    $(element).find('.cancel-button').bind('click', function(e) {
      runtime.notify('cancel', {});
      e.preventDefault();
    });
  }
