function discussion_dance(runtime, element)
{
    function on_post_press()
    {
        alert("Ajax call to be made!");

        var jqCommentBox = $(element).find("#usercomment");
        alert("Comment to be sent is " + jqCommentBox.val());
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'post_comment'),
            data: JSON.stringify({comment: jqCommentBox.val()}),
            success: function(result)
                    {
                        if(result.update_status == "Success")
                        {
                            alert("Database updated!");
                        }
                        else
                        {
                            alert("Database not updated! ret_val is " + result.update_status);
                        }
                    }
        });
    }

    function clear_comment_box(comment_box_id)
    {
        var jqCommentBox = $(element).find("#" + comment_box_id);
        jqCommentBox.val("");
    }

    $(element).find("#Post").bind('click',function()
        {
            on_post_press();
            clear_comment_box("usercomment");
        }
    );

    $(element).find("#Clear").bind('click',function()
        {
            clear_comment_box("usercomment");
        }
    );
}