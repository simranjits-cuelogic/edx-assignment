/* Javascript for DummyXBlock. */
function DummyXBlockStudio(runtime, element) {
    function reference_response(result) {
        console.log(result);
        // $('.dummyblock_block').closest('ul').append("<li>")
        alert(result.message);
    }

    $.fn.formData  = function(){
        return JSON.stringify({
                "reference" : $(this).getReferenceID(),
                "requested_action" : $(this).getRequestedAction()
            })
    }

    $.fn.getReferenceID  = function(){
        return $(this).closest('td').data('reference')
    }

    $.fn.getRequestedAction  = function(){
        return $(this).data('action')
    }

    var handlerUrl = runtime.handlerUrl(element, 'add_reference_to_course');

    $('a', element).click(function(eventObject) {
        var $thiss = $(this);

        eventObject.preventDefault();
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: $thiss.formData(),
            success: reference_response
        });
    });


}
