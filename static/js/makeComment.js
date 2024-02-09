
$(document).ready(function(){
    // subscriber button ajax call
    $('#feedbackForm').submit(function(e){
        e.preventDefault();
        $form = $(this)
        const token = $('input[name=csrfmiddlewaretoken').val()
        
        $.ajax({
            method:"POST",
            url: "/post_user_feedback/",
            headers:{'X-CSRFToken': token},
            data: {
                comment: $('#comment').val(),
                contentComment: $('#contentComment').val(),
            },
            success: function (data) {
                alert("Your feedback has been recorded")
                
            },
            error: function (data) {
                alert('Error: ' + "Occured");
            }
        })
    })
})
