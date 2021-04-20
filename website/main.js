var button = document.getElementById("button");

var $loading = $('#loadingDiv').hide();
var $note = $('#noteDiv').hide();

function processResponse(response){
    console.log(response)
    console.log(response.translated_text)
    document.getElementById("translated-text").innerHTML = response.translated_text
};

function ajax_wait() {
    document.getElementById("translated-text").innerHTML = ' ';
}

//Attach the loading gif to any element
$(document)
.ajaxStart(function () {
    $loading.show();
    $note.show(12000);
})
.ajaxStop(function () {
    $loading.hide();
    $note.hide();
});


button.addEventListener("click", function ajax_call() {

    var input = document.getElementById("text");
    var inputData = {
        "text": input.value
        }

    var src_lang = document.getElementById("src");
    var trg_lag = document.getElementById("trg");
    
    if (src_lang.value=="en" && trg_lag.value=="fr"){
        var condition = true
        var API_ENDPOINT = "PUBLIC-APIGATEWAY-LINK"
    }
    else if (src_lang.value=="fr" && trg_lag.value=="en"){
        var condition = true
        var API_ENDPOINT = "PUBLIC-APIGATEWAY-LINK"
    }
    else if (src_lang.value=="en" && trg_lag.value=="en"){
        var condition = false
        document.getElementById("translated-text").innerHTML = input.value
    }
    else if (src_lang.value=="fr" && trg_lag.value=="fr"){
        var condition = false
        document.getElementById("translated-text").innerHTML = input.value
    }
    else {
        var condition = false
        document.getElementById("translated-text").innerHTML = ' '
        alert("The option Spanish is not yet implemented. Please try with another language.")
    }

    console.log(inputData)
    console.log("Source language: " + src_lang.value)
    console.log("Target language: " + trg_lag.value)

    if (condition==true){
        $.ajax(
            {
            url: API_ENDPOINT,
            type: "POST",
            crossDomain: true,
            beforeSend: ajax_wait(),
            tryCount: 0,
            retryLimit: 5,
            contentType: "application/json",
            data: JSON.stringify(inputData),
            success: processResponse,
            error: function(xhr, status, error) {
                console.log("AJAX status:" + status)
                console.log("retry " + this.tryCount + " of " + this.retryLimit)
                if (status == 'error') {
                    this.tryCount++;
                    if (this.tryCount <= this.retryLimit) {
                        //try again
                        $.ajax(this);
                        return;
                    }
                    else {
                        alert("Something went wrong. Please refresh the page.");
                        return;
                    }
                }
                }
            }
            )
    }
}
);

function countWord() {
  
    // Get the input text value
    var words = document
        .getElementById("text").value;

    // Initialize the word counter
    var count = 0;

    // Split the words on each
    // space character 
    var split = words.split(' ');

    // Loop through the words and 
    // increase the counter when 
    // each split word is not empty
    for (var i = 0; i < split.length; i++) {
        if (split[i] != "") {
            count += 1;
        }
    }

    // Display it as output
    document.getElementById("show")
        .innerHTML = count;
}