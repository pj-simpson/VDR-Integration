// if there is no offset - 'first' is disabled, 'prev' is disabled, 'next is +10'
//if there is an offset, prev is -10 next is +10
//if there is an offset and its the same as the last offset, 'last is disabled' 'next' is disabled.

$( document ).ready(function() {
        var param = window.location.search;
        var paramArray = new URLSearchParams(param);

        if (paramArray.has('offset')) {
            //create a array of the key value pairs

            // get the current offset value
            var currentOffset = paramArray.get('offset');
            //get the final offset value
            var finalOffsetUrl = $("#last-pag-link").attr('href');
            var finalOffsetValue = finalOffsetUrl.replace('/sites/?offset=','');
            var prevOffsetValue = parseInt(currentOffset) - 10;
            paramArray.set('offset',prevOffsetValue)
            $("#prev-pag-link").attr("href", `/sites/?${paramArray.toString()}`);
            if (parseInt(currentOffset) === parseInt(finalOffsetValue)) {
                $("#last-pag-link").attr("disabled", "disabled");
                $("#next-pag-link").attr("disabled", "disabled");
                $("#last-pag-link").attr("href", "");
                $("#next-pag-link").attr("href", "");
            } else {
                var nextOffsetValue = parseInt(currentOffset) + 10;
                paramArray.set('offset',nextOffsetValue);
                console.log('I am here');
                $("#next-pag-link").attr("href", `/sites/?${paramArray.toString()}`);
            }

        } else {
            $("#first-pag-link").attr("disabled", "disabled");
            $("#prev-pag-link").attr("disabled", "disabled");
            $("#next-pag-link").attr("href", `/sites/?${paramArray.toString()}`+ '&offset=10');
        }

});