
    $('.join-button').on('click', function() {
        var forumId = $(this).data('forum-id');
        var button = $(this);
        console.log('Console here')
        // Send an AJAX request to the join_forum view
        $.ajax({
            url: '/forum/join_forum',
            type: 'GET',
            data: { forum: forumId },
            dataType: 'json',
            success: function(data) {
                // Update the button text and data attribute based on the response
                if (data.data === 'joined') {
                    button.text('joined');
                    button.data('forum-id', forumId);
                } else {
                    button.text('join');
                    button.data('forum-id', forumId);
                }
            },
            error: function(xhr, status, error) {
                // Handle errors here
                console.log('Error:', error);
            }
        });
    });


