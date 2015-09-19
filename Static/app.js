$(function() {
    $('button').click(function() {
        $.ajax({
            url: '/_submit_song',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    function updateListing() {
        var x = $.get( "/_get_song_listing.json", function(songs) {
            $(".vote_list").empty();
            console.log(songs);
            songs = $.parseJSON(songs);
            songs = songs["songs"];
            console.log(songs[0])
            for (i = 0; i<songs.length; i+=1) {
                $(".vote_list").append("<div class='song_vote_ranking'><div class='upvote-div'><div class='upvote-arrow'><img src='/static/upvote.png'></div><p class='upvotes'>" + songs[i]["upvotes"] + "</p><div class='downvote-arrow'><img src='/static/downvote.png'></div></div><div class='song-info'><p class='artist'>" + songs[i]["artist"] + "</p><p class='title'>" + songs[i]["title"] + "</p></div></div>");
            }

        });
    }
    updateListing()
    setInterval(function(){
        updateListing()
    },1000000);

});