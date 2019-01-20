$(document).ready(function () {

    $('.num').click(function () {
        var num = $(this);
        var text = $.trim(num.find('.txt').clone().children().remove().end().text());
        var telNumber = $('#telNumber');
        var telNumber2 = $('#accessKeyId');
        $(telNumber).val(telNumber.val() + text);
        $(telNumber2).val(telNumber2.val() + text);
        if (telNumber.val().length == 0 ) {
            document.getElementById("open-door-button").disabled = true;
        } else {
            document.getElementById("open-door-button").disabled = false;
        }
    });


    $('.backspace').click(function () {
        var num = $(this);
        var text = num.val();
        var telNumber = $('#telNumber');
        var telNumber2 = $('#accessKeyId');
        var value = telNumber.val();
        $(telNumber).val(value.substring(0, value.length - 1));
        $(telNumber2).val(value.substring(0, value.length - 1));
        if (telNumber.val().length == 0 ) {
            document.getElementById("open-door-button").disabled = true;
        } else {
            document.getElementById("open-door-button").disabled = false;
        }
    });

    $("#telNumber").keyup(function(){
        var fieldEntry = $('#telNumber').val();
        var postEntry = $('#accessKeyId');
        postEntry.val(fieldEntry)
        if (fieldEntry.length == 0 ) {
            document.getElementById("open-door-button").disabled = true;
        } else {
            document.getElementById("open-door-button").disabled = false;
        }
    });

});



