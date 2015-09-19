$(document).ready(function(){
    $('button').click(function() {

        $.ajax({
            url: '/_submit_song',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $(".form-add-song-message").empty()
                $(".form-add-song-message").append("<p>Song added ! (or was it already there?)</p>")
            },
            error: function(error) {
                $(".form-add-song-message").empty()
                $(".form-add-song-message").append("<p>Adding song failed</p>")
            }
        });
    });

    function updateListing() {
        var x = $.get( "/_get_song_listing.json", function(songs) {
            $(".vote_list").empty();
            songs = $.parseJSON(songs);
            songs = songs["songs"];
            for (i = 0; i<songs.length; i+=1) {
                $(".vote_list").append("<div class='song_vote_ranking'><div class='upvote-div'><div class='upvote-arrow'><img src='/static/upvote.png'></div><div class='downvote-arrow'><img src='/static/downvote.png'></div></div><div class='song-info'><p class='upvotes'>" + songs[i]["upvotes"] + "</p><p class='artist'>" + songs[i]["artist"] + "</p><p class='title'>" + songs[i]["title"] + "</p></div></div>");
            }


        });
    }

    function updatePlaylist() {
        var x = $.get( "/_get_playlist_listing.json", function(songs) {
            $(".play_list").empty();
            songs = $.parseJSON(songs);
            songs = songs["songs"]
            for (i = 0; i<songs.length; i+=1) {
                $(".play_list").append("<div class='song-container'><p class='upvotes'>" + songs[i]["upvotes"] + "</p><p class='artist'>" + songs[i]["artist"] + "</p><p class='title'>" + songs[i]["title"] + "</p></div>");
            }

        });
    }

    $(".vote_list").on("click", ".upvote-arrow", function(){
        var info = {}
        info["title"] = $(this).parent().parent().find(".song-info .title").text()
        info["artist"] = $(this).parent().parent().find(".song-info .artist").text()
        $.ajax({
            url: '/_upvote_song',
            data: JSON.stringify(info, null, "\t"),
            contentType: 'application/json;charset=UTF-8',
            type: 'POST',
        });
        var value = parseInt($(this).parent().parent().find("p.upvotes").text())+1
        $(this).parent().parent().find("p.upvotes").text(value)

    });

    $(".vote_list").on("click", ".downvote-arrow", function(){
        var info = {}
        info["title"] = $(this).parent().parent().find(".song-info .title").text()
        info["artist"] = $(this).parent().parent().find(".song-info .artist").text()
        $.ajax({
            url: '/_downvote_song',
            data: JSON.stringify(info, null, "\t"),
            contentType: 'application/json;charset=UTF-8',
            type: 'POST',
        });
        var value = parseInt($(this).parent().parent().find("p.upvotes").text())-1
        $(this).parent().parent().find("p.upvotes").text(value)
    });

    updateListing()
    updatePlaylist()

    setInterval(function(){
        updateListing()
    },30*1000);

    setInterval(function(){
        updatePlaylist()
    },30*1000);

});