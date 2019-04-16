function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $(".js-like-article").on("click", function() {
        var $this = $(this);
        $.ajax({
            url: "/like_article/",
            method: "POST",
            dataType: "json",
            data: {
                "article_id": $this.data("article_id"),
                "csrfmiddlewaretoken": getCookie("csrftoken")
            }
        }).done(function(data) {
            console.log(data);
            location.reload();
        });
        return false;
    });

    var centrifuge = new Centrifuge('ws://127.0.0.1:8001/connection/websocket');

    centrifuge.subscribe("new_posts", function(message) {
        alert(message.data.article_text)
    });

    centrifuge.connect();
});
