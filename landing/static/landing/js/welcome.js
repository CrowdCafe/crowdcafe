function fadedEls(el, shift) {
    el.css('opacity', 0);

    switch (shift) {
        case undefined: shift = 0;
        break;
        case 'h': shift = el.eq(0).outerHeight();
        break;
        case 'h/2': shift = el.eq(0).outerHeight() / 2;
        break;
    }

    $(window).resize(function() {
        if (!el.hasClass('ani-processed')) {
            el.eq(0).data('scrollPos', el.eq(0).offset().top - $(window).height() + shift);
        }
    }).scroll(function() {
        if (!el.hasClass('ani-processed')) {
            if ($(window).scrollTop() >= el.eq(0).data('scrollPos')) {
                el.addClass('ani-processed');
                el.each(function(idx) {
                    $(this).delay(idx * 200).animate({
                        opacity : 1
                    }, 1000);
                });
            }
        }
    });
};

(function($) {
    $(function() {

        // Sections height & scrolling
        $(window).resize(function() {
            var sH = $(window).height();
            $('section.header-10-sub').css('height', (sH - $('header').outerHeight()) + 'px');
           // $('section:not(.header-10-sub):not(.content-11)').css('height', sH + 'px');
       });        

        // Parallax
        $('.header-10-sub, .content-23').each(function() {
            $(this).parallax('50%', 0.3, true);
        });

        // Faded elements
        fadedEls($('.welcome-block-categories'), 300);
        fadedEls($('.welcome-block-contexts'), 300);
        fadedEls($('.welcome-block-opensource'), 300);
        fadedEls($('.welcome-block-philosophy'), 300);
        fadedEls($('.welcome-block-rewards'), 300);

        // Ani screen
        (function(el) {
            $('img:first-child', el).css('left', '-29.7%');

            
        })($('.screen'));


        (function(el) {
            el.css('left', '-100%');

            $(window).resize(function() {
                if (!el.hasClass('ani-processed')) {
                    el.data('scrollPos', el.offset().top - $(window).height() + el.outerHeight());
                }
            }).scroll(function() {
                if (!el.hasClass('ani-processed')) {
                    if ($(window).scrollTop() >= el.data('scrollPos')) {
                        el.addClass('ani-processed');
                        el.animate({
                            left : 0
                        }, 500);
                    }
                }
            });
        });
        $(window).resize().scroll();

    });

$(window).load(function() {
    $('html').addClass('loaded');
    $(window).resize().scroll();
    $('.social-feed-container').socialfeed({
        template:social_feed_template,
                      //FACEBOOK--------------------
                      facebook:{
                          accounts:['@crowdcafe.io','#crowdcafe.io'], //usernames or id
                          limit:5,
                          token:'240696342763428|FgHgjfn7wWMNT15ONHP0tVdWm_k' //you can also create an app and put  here your 'APP ID|APP SECRET' - it is easier but not safe
                      },
                      //INSTAGRAM---------------------
                      instagram:{
                        accounts:['#coffeetask'], //userid
                        client_id:'2c6d2173ae9d41de905236e6301e5a43', //2c6d2173ae9d41de905236e6301e5a43
                        limit:2
                    },
                      //GENERAL SETTINGS--------------
                      length:250,
                      show_media:true,
                      callback: function(){
                          console.log('all posts are collected');
                      }
                  });
});

})(jQuery);



