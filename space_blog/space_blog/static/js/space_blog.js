                // Fixed navbar on scroll -------------------------------------------------
                (function($) {
                  "use strict";

                  // Floating label headings for the contact form
                  $("body").on("input propertychange", ".floating-label-form-group", function(e) {
                    $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
                  }).on("focus", ".floating-label-form-group", function() {
                    $(this).addClass("floating-label-form-group-with-focus");
                  }).on("blur", ".floating-label-form-group", function() {
                    $(this).removeClass("floating-label-form-group-with-focus");
                  });

                  // Show the navbar when the page is scrolled up
                  var MQL = 992;

                  //primary navigation slide-in effect
                  if ($(window).width() > MQL) {
                    var headerHeight = $('#mainNav').height();
                    $(window).on('scroll', {
                        previousTop: 0
                      },
                      function() {
                        var currentTop = $(window).scrollTop();
                        //check if user is scrolling up
                        if (currentTop < this.previousTop) {
                          //if scrolling up...
                          if (currentTop > 0 && $('#mainNav').hasClass('is-fixed')) {
                            $('#mainNav').addClass('is-visible');
                          } else {
                            $('#mainNav').removeClass('is-visible is-fixed');
                          }
                        } else if (currentTop > this.previousTop) {
                          //if scrolling down...
                          $('#mainNav').removeClass('is-visible');
                          if (currentTop > headerHeight && !$('#mainNav').hasClass('is-fixed')) $('#mainNav').addClass('is-fixed');
                        }
                        this.previousTop = currentTop;
                      });
                  }

                })(jQuery); // End of use strict

                // Lazy load blog posts ---------------------------------------------------
                (function($) {
                    $('#lazyLoadLink').on('click', function() {
                        var link = $(this);
                        var page = link.data('page');

                        link.hide();
                        $('#loadingImg').show();

                        function ajaxCall() {
                            $.ajax({
                                type: 'post',
                                url: '/lazy_load_posts/',
                                data: {
                                  'page': page,
                                  'query': link.data('query'),
                                  'category': link.data('category'),
                                  'csrfmiddlewaretoken': window.CSRF_TOKEN // from base.html
                                },
                                success: function(data) {
                                    // if there are still more pages to load,
                                    // add 1 to the "Load More Posts" link's page data attribute
                                    // else hide the link
                                    if (data.has_next) {
                                        link.data('page', page+1);
                                        link.show();
                                    } else {
                                        link.hide();
                                        $('#scrollToTopLink').show();
                                    }
                                    // append html to the posts div

                                    $('#posts').append(data.posts_html);
                                },
                                error: function(xhr, status, error) {
                                  // shit happens friends!
                                    console.log("Oops")
                                },
                                complete: function (data) {
                                    $('#loadingImg').hide();
                                }
                            });
                        }
                        setTimeout(ajaxCall, 1000);
                    });
                }(jQuery));

                // Scroll to top
                (function ($) {
                    $('#scrollToTopLink').on('click', function () {
                        $('html,body').animate({scrollTop:0}, 'slow');
                    });
                })(jQuery);
