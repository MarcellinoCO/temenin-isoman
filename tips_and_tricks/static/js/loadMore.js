  // Load More
$(document).ready(function() {
    $("#loadmoreBtn").on('click', function() {
        var _currentResult = $(".post-box").length;
        $.ajax({
            url: "/tips-and-tricks/load-more",
            type: 'GET',
            data: {
                'offset': _currentResult,
            },
            dataType: 'json',
            beforeSend: function() {
                $("#loadmoreBtn").addClass('disabled').text('Loading..');
            },
            success: function(res) {
                var _html = '';
                var json_data = $.parseJSON(res.posts);
                $.each(json_data, function(index, data) {
                    _html += `<div
                                class="card p-3 mt-4 post-box"
                                id="article-list"
                            >
                                <div class="row">
                                    <div class="col-md-4">
                                        <div class="position-relative">
                                        <img
                                            height="230"
                                            src= ${data.fields.image_url}
                                            class="rounded w-100"
                                        >
                                        </div>
                                    </div>
                                    <div class="col-md-8">
                                        <div class="mt-2">
                                            <div class="d-flex justify-content-between align-items-center">
                                                <h5 class="mb-1"> ${data.fields.title}</h5>
                                            </div>
                                            <div class="d-flex justify-content-md-start justify-content-between views-content mt-2">
                                                <div class="d-flex flex-row align-items-center"> <i class="fa fa-calendar"></i> <span class="ms-1 views"> ${data.fields.published_date}</span> </div>
                                                <div class="d-flex flex-row align-items-center ms-2"> <i class="fa fa-user"></i> <span class="ms-1 views"> ${ data.fields.source}</span> </div>
                                            </div>
                                            <p class="text-dark mt-3"> ${data.fields.brief_description}</p>
                                            <a
                                                class="btn btn-sm btn-dark"
                                                target="_blank"
                                                href="${data.fields.article_url}"
                                                class="align-self-end btn btn-sm btn-block btn-dark"
                                            >Lanjut Membaca</a>
                                        </div>
                                    </div>
                                </div>
                            </div>`;
                });
                $("#replaceable-content").append(_html);
                var _countTotal = $(".post-box").length;
                if (_countTotal == res.totalResult) {
                    $("#loadmoreBtn").hide();
                }
                $("#loadmoreBtn").removeClass('disabled').text('Load More');
            }
        });
    });
});