(function(){
    $('input[type="button"]').on('click', function(){
        var $this = $(this),
            edit_status = $this.attr('edit_status'),
            status_value = edit_status && 1 == edit_status ? 0 : 1,
            $td_arr = $this.parent().prevAll('td');
        $this.val(1 == status_value ? 'complete' : 'edit').attr('edit_status', status_value);
        $.each($td_arr, function(){
            var $td = $(this);
            if(1 == status_value) {
                $td.html('<input type="text" value="'+$td.html()+'">');
            } else if(0 == status_value){
                $td.html($td.find('input[type=text]').val());
            }
        });
    });
})();