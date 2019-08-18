function enableDropOff() {
    $("#pickupForm").show();
    $("#dropoffForm").hide();
}

function enablePickup() {
    $("#dropoffForm").show();
    $("#pickupForm").hide();
}


// https://www.sitepoint.com/url-parameters-jquery/
//URL is http://www.example.com/mypage?ref=registration&email=bobo@example.com
$.urlParam = function (name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)')
                      .exec(window.location.search);

    return (results !== null) ? results[1] || 0 : false;
}


function selectLocation() {
    var location = $.urlParam('loc');

    if ((location) && (location === '2')) {
        $("#closetLocation").val('Oak Ridge');
    }
}