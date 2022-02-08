// if there are query params in the url - pre select the option drop-down
$( document ).ready(function() {
    if(document.location.search.length) {
        var param = window.location.search;
        var paramArray = new URLSearchParams(param);
        if (paramArray.has('status')) {
            var statusValue  = paramArray.get('status')
            $("#site-status").val('/sites/?status=' + statusValue);
        }
    } else {
        $("#site-status").val('/sites/');
    }
});


//if the site status drop down changes - fire the link from the option selection
$( "#site-status" ).change(function(event) {
    // this ensures that its only a change which comes from the user and not other jquery
    if (event.originalEvent){
        var url = $(this).val();
          if (url) {
              window.location = url;
          }
    }
});

//function to intercept clicks of disabled links:

$("a").on("click", function(event){
    if ($(this).is("[disabled]")) {
        event.preventDefault();
    }
});





