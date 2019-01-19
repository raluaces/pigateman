$(document).ready(function () {

    $('.num').click(function () {
        var num = $(this);
        var text = $.trim(num.find('.txt').clone().children().remove().end().text());
        var telNumber = $('#telNumber');
        var telNumber2 = $('#accessKeyId');
        $(telNumber).val(telNumber.val() + text);
        $(telNumber2).val(telNumber2.val() + text);
    });


    $('.backspace').click(function () {
        var num = $(this);
        var text = num.val();
        var telNumber = $('#telNumber');
        var telNumber2 = $('#accessKeyId');
        var value = telNumber.val();
        console.log(value.length);
        $(telNumber).val(value.substring(0, value.length - 1));
        $(telNumber2).val(value.substring(0, value.length - 1));
    });

    $("#telNumber").keyup(function(){
        var fieldEntry = $('#telNumber').val();
        console.log(fieldEntry);
        var postEntry = $('#accessKeyId');
        postEntry.val(fieldEntry)
    });

});



