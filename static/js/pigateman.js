
// Document Dot Ready
$(document).ready(function() {
    $('#open-door').submit(function(event){
        event.preventDefault();
        //console.log('');
        postData = $('#open-door').serialize();
        postDoorData(postData);
    });



});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function restore_button() {
    await sleep(3000);
    document.getElementById("open-door-button").classList.remove('btn-danger');
    document.getElementById("open-door-button").classList.add('btn-primary');
    document.getElementById("open-door-button").disabled = false;
    document.getElementById("open-door-button").firstChild.data = 'ENTER'
    $('#progresstimebar')
        .css("width", "100%")
        .attr("aria-valuenow", document.getElementById('open-door').unlockTime.value);
}

function postDoorData(postData) {
    $.ajax({
        type: 'POST',
        url: '/door/open/',
        data: postData,
        beforeSend: function( jqXHR ) {
            //  console.log('beforeSend');
            document.getElementById("open-door-button").disabled = true;
            document.getElementById("open-door-button").hidden = true;
            try {
                document.getElementById("alertBox").textContent = '';
                document.getElementById("alertBox").hidden = true;
                document.getElementById("keyPadId").hidden = true;
            }catch(err){}
            document.getElementById("progressWhole").hidden = false;
            document.getElementById("open-door-button").classList.add('btn-success');
            document.getElementById("open-door-button").classList.remove('btn-primary');
            document.getElementById("open-door-button").firstChild.data = 'Door Unlocked.'
            ProgressCountdown(document.getElementById('open-door').unlockTime.value, 'progresstimebar', 'progresstimebar');

        },
        success: function(data, textStatus, postData) {
            // console.log('success: '+data);
            document.getElementById("progresstimebar").textContent = '';
            document.getElementById("open-door-button").firstChild.data = 'Door Locked'
            document.getElementById("open-door-button").classList.remove('btn-success');
            document.getElementById("open-door-button").classList.add('btn-info');
            document.getElementById("progresstimebar").textContent = '';
            try {
                document.getElementById("keypadCard").hidden = false;
                document.getElementById("messageBody").innerHTML = data;
            } catch {}
        },
        error: function(data, textStatus, errorThrown) {
            // console.log('error: '+data.responseText);
            try {
                document.getElementById("keyPadId").hidden = false;
            }catch(err){}
            document.getElementById("progressWhole").hidden = true;
            document.getElementById("open-door-button").hidden = false;
            document.getElementById("open-door-button").classList.remove('btn-success');
            document.getElementById("open-door-button").classList.add('btn-danger');
            document.getElementById("open-door-button").firstChild.data = 'BAD KEY'
            $('#telNumber').val('');
            $('#accessKeyId').val('');
            restore_button();
            document.getElementById("alertBox").textContent = data.responseText;
            document.getElementById("alertBox").hidden = false;
        },
        complete: function(){
            // console.log('complete');

        }
    });
}

function ProgressCountdown(timeleft, bar, text) {
    var timeleftinitial = timeleft;
    $('#progresstimebar').attr("aria-valuemax", timeleft);
    return new Promise((resolve, reject) => {
        var interval = 32;
        var countdownTimer = setInterval(() => {
            timeleft -= interval / 1000.0;
            $('#progresstimebar')
                .css("width", (100 / timeleftinitial) * timeleft + "%")
                .attr("aria-valuenow", timeleft);
            document.getElementById(text).textContent = timeleft.toFixed(0);

            if (timeleft <= 0) {
                clearInterval(countdownTimer);
                resolve(true);
                document.getElementById("progressWhole").hidden = true;
            }
            if (document.getElementById("open-door-button").firstChild.data == 'BAD KEY') {
                clearInterval(countdownTimer);
                resolve(true);
            }
        }, interval);
    });
}