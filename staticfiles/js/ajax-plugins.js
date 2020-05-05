$(document).ready(function() {
    $('#general-entry').click(function(){
        $.ajax({
            url: 'general-entry/',
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal').modal('show');
            },
            success: function(data) {
                $('#modal .modal-content').html(data.html_form);
            }
        });
    });

    $('#modal').on('submit', '.add-entry', function() {
        var form = $(this);
        $.ajax({
            url : form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
              if(data.form_is_valid){
                $('#entry_list tbody').html(data.entry_list);
                console.log(data.entry_list);
                $('#modal').modal('hide');
                console.log('sucess its been save');
              }
              else {
                $('#modal', '.modal-content').html(data.html_form);
              }
            }
        });
        return false;
    });
});
