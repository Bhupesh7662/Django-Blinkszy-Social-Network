// Deleting normal post
function delete_data(id) {
    $.ajax({
        url: 'http://localhost:8000/userpage/delete_post/' + id,
        success: function () {
            $("#" + id).fadeOut(500);
        }
    });
}

// Deleting hot post
function delete_hot_data(id) {
    $.ajax({
        url: 'http://localhost:8000/hotornot/delete_hot_post/' + id,
        success: function () {
            $("#" + id).fadeOut(500);
        }
    });
}


// Deleting post comment
function delete_comment_data(id) {
    $.ajax({
        url: 'http://localhost:8000/userpage/delete_post_comment/' + id,
        success: function (result) {
            if (result == 'success') {
                $("#" + id).fadeOut(500);
                $('#comment_' + id).hide();
            }
        }
    });
}

// Deleting hot comment
function delete_hot_comment_data(id) {
    $.ajax({
        url: 'http://localhost:8000/hotornot/delete_hot_comment/' + id,
        success: function (result) {
            if (result == 'success') {
                $("#" + id).fadeOut(500);
                $('#comment_' + id).hide();
            }
        }
    });
}

// Liking normal post
$(".like").click(function (e) {
    var id = this.id;
    var href = $('.like').find('a').attr('href');
    e.preventDefault();
    $.ajax({
        url: href,
        data: {
            'post_id': id
        },
        success: function (response) {
            if (response.liked) {
                $('#likebtn' + id).html("❤"); //liked 
            } else {
                $('#likebtn' + id).html("like"); //like
            }
        }
    })
});

// Follow unfollow user
$(".follow").click(function (e) {
    e.preventDefault();
    var href = this.href;
    console.log(href);
    $.ajax({
        url: href,
        success: function (response) {
            console.log(response);
            if (response["following"]) {
                $("#follow").html("&#10003; Following");
            } else {
                $("#follow").html("+ Follow");
            }
        }
    })
});