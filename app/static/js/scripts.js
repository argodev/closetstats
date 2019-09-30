function enablePickup() {
    $("#pickupForm").show();
    $("#dropoffForm").hide();
    $("#pickUpBtn").hide();
    $("#dropOffBtn").hide();
    $("#visitType").val("pickup");
}

function enableDropoff() {
    $("#dropoffForm").show();
    $("#pickupForm").hide();
    $("#pickUpBtn").hide();
    $("#dropOffBtn").hide();
    $("#visitType").val("dropoff");
}

function resetForm() {
    form.reset();
    $("#pickUpBtn").show();
    $("#dropOffBtn").show();
    $("#dropoffForm").hide();
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

// https://lengstorf.com/get-form-values-as-json/

/**
 * Retrieves input data from a form and returns it as a JSON object
 * @param {HTMLFormControlsCollection} elements the form elements
 * @return {Object}  form data as an object literal
 */
const formToJSON = elements => [].reduce.call(elements, (data, element) => {
    if (element.name) {
        if (element.type === "checkbox") {
            data[element.name] = element.checked;
        } else {
            data[element.name] = element.value;
        }
    }
    return data;
}, {});



/**
 * A handler function to prevent default submission and run our custom script.
 * @param {Event} event the submit event triggered by the user
 * @param {void}
 */
const handleFormSubmit = event => {
    // stop the form from submitting since we are handling it
    event.preventDefault();

    // TODO: Call our function to get the form data
    const data = formToJSON(form.elements);

    console.log(data);

    // this is where we will actually do something with the form
    $.ajax({
        type: "POST",
        url: "/api/visit",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
            resetForm();
        },
        error: function(response, status, error) {
            alert("Update Failed! Please try again in a few moments \n(" + error + ")");
        }
    });
}

/**
 * This is where things actually get started. We find the form element using 
 * its name, then attach the `handleFormSubmit()` function to the
 * `submit` event
 */
const form = document.getElementsByClassName('visit-form')[0];
form.addEventListener('submit', handleFormSubmit);
