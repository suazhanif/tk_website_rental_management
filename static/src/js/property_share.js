$(document).ready(function() {
    $('.share_twitter, .share_facebook, .share_linkedin').on('click', function(ev) {
        ev.preventDefault();
        var url = '';
        var $element = $(this);
        var blogPostTitle = $('#property-name').html() || '';
        var articleURL = window.location.href;
        if ($element.hasClass('share_twitter')) {
            var tweetText =
                "Amazing property: %s! Check it live: %s",
                blogPostTitle,
                articleURL
            ;
            url = 'https://twitter.com/intent/tweet?tw_p=tweetbutton&text=' + encodeURIComponent(tweetText);
        } else if ($element.hasClass('share_facebook')) {
            url = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(articleURL);
        } else if ($element.hasClass('share_linkedin')) {
            url = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(articleURL);
        }
        window.open(url, '', 'menubar=no, width=1000, height=500');
    })
})
