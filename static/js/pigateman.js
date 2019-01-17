
// Document Dot Ready
$(document).ready(function() {
    $('#open-door').submit(function(event){
        event.preventDefault();
        //console.log('');
        postData = $('#open-door').serialize();
        console.log(postData);
        postDoorData(postData);
    });

});



function postDoorData(postData) {
    $.ajax({
        type: 'POST',
        url: '/door/open/',
        data: postData,
        beforeSend: function( jqXHR ) {
            //  console.log('beforeSend');
            document.getElementById("open-door-button").disabled = true;
            document.getElementById("open-door-button").hidden = true;
            document.getElementById("progressWhole").hidden = false;
            document.getElementById("open-door-button").classList.add('btn-success');
            document.getElementById("open-door-button").classList.remove('btn-primary');
            document.getElementById("open-door-button").firstChild.data = 'Door Unlocked.'
            ProgressCountdown(7, 'progresstimebar', 'progresstimebar');

        },
        success: function(data, textStatus, postData) {
            // console.log('success: '+data);
            document.getElementById("open-door-button").firstChild.data = 'Door Locked'
            document.getElementById("open-door-button").classList.remove('btn-success');
            document.getElementById("open-door-button").classList.add('btn-info');
        },
        error: function(data, textStatus, errorThrown) {
            // console.log('error: '+data.responseText);
            document.getElementById("open-door-button").false = true;
            document.getElementById("open-door-button").classList.remove('btn-success');
            document.getElementById("open-door-button").classList.add('btn-danger');
            document.getElementById("open-door-button").firstChild.data = 'Problem unlocking  door.'
        },
        complete: function(){
            // console.log('complete');

        }
    });
}

function ProgressCountdown(timeleft, bar, text) {
    var timeleftinitial = timeleft;
    return new Promise((resolve, reject) => {
        var countdownTimer = setInterval(() => {
            timeleft--;

            $('#progresstimebar')
                .css("width", (100 / timeleftinitial) * timeleft + "%")
                .attr("aria-valuenow", timeleft);
            document.getElementById(text).textContent = timeleft;

            if (timeleft <= 0) {
                clearInterval(countdownTimer);
                resolve(true);
            }
        }, 1000);
    });
}