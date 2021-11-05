// Search
$(document).ready(function() {
    $("#searchBtn").on('click', function() {
        $.ajax({
            url: "/tips-and-tricks",
            type: 'GET',
            data: {
                'q': $("#user-input").val(),
            },
            beforeSend: function() {
                $("#searchBtn").addClass('disabled').text('Loading..');
            },
            success: function(res) {
                if ($("#user-input").val() != '') {
                    $("#loadmoreBtn").hide();
                    _html = '<p class="mt-5 display-6"> Search Result for keywords \'' + $("#user-input").val() + '\'<p>';
                } else {
                    $("#loadmoreBtn").show();
                    _html = '';
                }
                
                $("#replaceable-content").html(_html + res['html_from_view']);
                $("#searchBtn").removeClass('disabled').text('Search');

                if ($(".post-box").length == 0) {
                    var userInput = $("#user-input").val();
                    $("#replaceable-content").html(`
                        <div class="text-center mt-6">
                            <i class="fa fa-search fa-6x""></i>
                            <p class="lead mt-1">No Article Available for keywords \'${userInput}\'</p>
                        </div>`);
                }
            }
        });
    });
});