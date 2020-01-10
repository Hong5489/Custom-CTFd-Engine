window.challenge.data = undefined;

window.challenge.renderer = new markdownit({
    html: true,
});

window.challenge.preRender = function () {

};

window.challenge.render = function (markdown) {
    return window.challenge.renderer.render(markdown);
};


window.challenge.postRender = function () {

};


window.challenge.submit = function (cb, preview) {
    var challenge_id = parseInt($('#challenge-id').val());
    var submission = $('#submission-input').val();
    var url = "/api/v1/challenges/attempt";

    if (preview) {
        url += "?preview=true";
    }

    var params = {
        'challenge_id': challenge_id,
        'submission': submission
    };

    CTFd.fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response.json();
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response.json();
        }
        return response.json();
    }).then(function (response) {
        cb(response);
    });
};

function managePort() {
    var port = document.getElementById("port");
    port.disabled = true;
    var challenge_id = parseInt($('#challenge-id').val());
    document.getElementById("port-status").innerHTML = "Loading...";
    var url = "/api/v1/challenges/ports";

    var params = {
        'challenge_id': challenge_id,
    };
    if(!port.checked){
        url += "?close=true";
    }
    CTFd.fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response.json();
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response.json();
        }
        return response.json();
    }).then(function (response) {
        renderSubmissionResponse(response);
        if(!port.checked){
            document.getElementById("port-status").innerHTML = "Closed";
        }else{
            var number = response.data.number.toString();
            document.getElementById("port-status").innerHTML = "Opened in this " + '<a href="http://skrctf.me/ports/'+ number +'/" target="_blank">Website</a>';
            console.log(number);
        }
        port.disabled = false;
    });
};