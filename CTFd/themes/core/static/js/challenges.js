var challenges;
var user_solves = [];
var templates = {};

window.challenge = new Object();

function loadchal(id) {
    var obj = $.grep(challenges, function (e) {
        return e.id == id;
    })[0];

    if (obj.type === 'hidden') {
        ezal({
            title: "Challenge Hidden!",
            body: "You haven't unlocked this challenge yet!",
            button: "Got it!"
        });
        return;
    }
    if (obj.lock){
        ezal({
            title: "Challenge Locked!",
	    body: "You need to solve <b>"+obj.requirement+"</b> to unlock this challenge!",
            button: "Got it!"
        });
        return;
    }

    updateChalWindow(obj);
}

function loadchalbyname(chalname) {
    var obj = $.grep(challenges, function (e) {
        return e.name == chalname;
    })[0];

    updateChalWindow(obj);
}

function updateChalWindow(obj) {
    $.get(script_root + "/api/v1/challenges/" + obj.id, function (response) {
        var challenge_data = response.data;

        $.getScript(script_root + obj.script, function () {
            $.get(script_root + obj.template, function (template_data) {
                $('#challenge-window').empty();
                var template = nunjucks.compile(template_data);
                window.challenge.data = challenge_data;
                window.challenge.preRender();

                challenge_data['description'] = window.challenge.render(challenge_data['description']);
                challenge_data['script_root'] = script_root;

                $('#challenge-window').append(template.render(challenge_data));

                $('.challenge-solves').click(function (e) {
                    getsolves($('#challenge-id').val())
                });
                $('.nav-tabs a').click(function (e) {
                    e.preventDefault();
                    $(this).tab('show')
                });

                // Handle modal toggling
                $('#challenge-window').on('hide.bs.modal', function (event) {
                    $("#submission-input").removeClass("wrong");
                    $("#submission-input").removeClass("correct");
                    $("#incorrect-key").slideUp();
                    $("#correct-key").slideUp();
                    $("#already-solved").slideUp();
                    $("#too-fast").slideUp();
                });

                $('#submit-key').click(function (e) {
                    e.preventDefault();
                    $('#submit-key').addClass("disabled-button");
                    $('#submit-key').prop('disabled', true);
                    window.challenge.submit(function (data) {
                        renderSubmissionResponse(data);
                        /*loadchals(function () {
                            marksolves();
                        });*/
                        marksolves();
                    });
                });

                $("#submission-input").keyup(function (event) {
                    if (event.keyCode == 13) {
                        $("#submit-key").click();
                    }
                });


                $(".input-field").bind({
                    focus: function () {
                        $(this).parent().addClass('input--filled');
                        $label = $(this).siblings(".input-label");
                    },
                    blur: function () {
                        if ($(this).val() === '') {
                            $(this).parent().removeClass('input--filled');
                            $label = $(this).siblings(".input-label");
                            $label.removeClass('input--hide');
                        }
                    }
                });

                window.challenge.postRender();

                window.location.replace(window.location.href.split('#')[0] + '#' + obj.name);
                $('#challenge-window').modal();


                $('.challenge-writeup').click(function (e) {
                    getwriteups($('#challenge-id').val())
                });



                $('#submit-link').click(function (e) {
                    var link = $('#link-input').val();
                    var id = $('#challenge-id').val();
                    var params = {
                        'link': link
                    };
                    ezq({
                        title: "Post Writeup",
                        body: "Are you sure you want to post the writeup link {0}?".format("<strong>" + htmlentities(link) + "</strong>"),
                        success: function () {
                            CTFd.fetch('/api/v1/challenges/' + id + '/writeup', {
                                method: 'POST',
                                body: JSON.stringify(params)
                            }).then(function (response) {
                                return response.json();
                            }).then(function (response) {
                                if (response.success) {
                                    ezal({
                                        title: "Post Writeup",
                                        body: "Successfully posted your writeup link",
                                        button: "Got it!",
                                        success: function(){
                                            document.location.reload(true);
                                            console.log("fcuk");
                                        }
                                    });
                                }else{
                                    ezal({
                                        title: "Post Writeup",
                                        body: "Failed to post your writeup link",
                                        button: "Got it!"
                                    });
                                }
                            });
                        }
                    });
                });
            });
        });
    });
}

$("#submission-input").keyup(function (event) {
    if (event.keyCode == 13) {
        $("#submit-key").click();
    }
});


function renderSubmissionResponse(response, cb) {
    var result = response.data;

    var result_message = $('#result-message');
    var result_notification = $('#result-notification');
    var answer_input = $("#submission-input");
    result_notification.removeClass();
    result_message.text(result.message);

    if (result.status === "authentication_required") {
        window.location = script_root + "/login?next=" + script_root + window.location.pathname + window.location.hash;
        return
    }
    else if (result.status === "incorrect") { // Incorrect key
        result_notification.addClass('alert alert-danger alert-dismissable text-center');
        result_notification.slideDown();

        answer_input.removeClass("correct");
        answer_input.addClass("wrong");
        setTimeout(function () {
            answer_input.removeClass("wrong");
        }, 3000);
    }
    else if (result.status === "correct") { // Challenge Solved
        result_notification.addClass('alert alert-success alert-dismissable text-center');
        result_notification.slideDown();

        $('.challenge-solves').text((parseInt($('.challenge-solves').text().split(" ")[0]) + 1 + " Solves"));

        answer_input.val("");
        answer_input.removeClass("wrong");
        answer_input.addClass("correct");
    }
    else if (result.status === "already_solved") { // Challenge already solved
        result_notification.addClass('alert alert-info alert-dismissable text-center');
        result_notification.slideDown();

        answer_input.addClass("correct");
    }
    else if (result.status === "paused") { // CTF is paused
        result_notification.addClass('alert alert-warning alert-dismissable text-center');
        result_notification.slideDown();
    }
    else if (result.status === "ratelimited") { // Keys per minute too high
        result_notification.addClass('alert alert-warning alert-dismissable text-center');
        result_notification.slideDown();

        answer_input.addClass("too-fast");
        setTimeout(function () {
            answer_input.removeClass("too-fast");
        }, 3000);
    }
    setTimeout(function () {
        $('.alert').slideUp();
        $('#submit-key').removeClass("disabled-button");
        $('#submit-key').prop('disabled', false);
    }, 3000);

    if (cb) {
        cb(result);
    }
}

function marksolves(cb) {
    $.get(script_root + '/api/v1/' + user_mode + '/me/solves', function (response) {
        var solves = response.data;
        for (var i = solves.length - 1; i >= 0; i--) {
            var id = solves[i].challenge_id;
            var btn = $('button[value="' + id + '"]');
            btn.addClass('solved-challenge');
            btn.prepend("<i class='fas fa-check corner-button-check'></i>")
        }
        if (cb) {
            cb();
        }
	    });
}

function load_user_solves(cb) {
    if (authed) {
        $.get(script_root + '/api/v1/' + user_mode + '/me/solves', function (response) {
            var solves = response.data;

            for (var i = solves.length - 1; i >= 0; i--) {
                var chal_id = solves[i].challenge_id;
                user_solves.push(chal_id);

            }
            if (cb) {
                cb();
            }
        });
    } else {
        cb();
    }
}

function getsolves(id) {
    $.get(script_root + '/api/v1/challenges/' + id + '/solves', function (response) {
        var data = response.data;
        $('.challenge-solves').text(
            (parseInt(data.length) + " Solves")
        );
        var box = $('#challenge-solves-names');
        box.empty();
        for (var i = 0; i < data.length; i++) {
            var id = data[i].account_id;
            var name = data[i].name;
            var date = moment(data[i].date).local().fromNow();
            var account_url = data[i].account_url
            box.append('<tr><td><a href="{0}">{2}</td><td>{3}</td></tr>'.format(account_url, id, htmlentities(name), date));
        }
    });
}

function getwriteups(id) {
    $.get(script_root + '/api/v1/challenges/' + id + '/writeup', function (response) {
        var data = response.data;
        var box = $('#challenge-writeup-names');
        box.empty();
        for (var i = 0; i < data.length; i++) {
            var name = data[i].author;
            var account_url = data[i].account_url;
            var link = data[i].link;
            box.append('<tr><td><a href="{0}" target="_blank" style="word-break: break-word;">{1}</td><td><a href="{2}">{3}</td></tr>'.format(htmlentities(link),htmlentities(link),account_url,htmlentities(name)));
        }
    });
}


function clickLike(likeCount,liked){
    if(liked){
        likeCount--;
    }
    if($('#likes').attr('style')){
        $('#likes').attr('style',"");
        $('#likeCount').html(" "+(likeCount))
    }else{
        $('#likes').attr('style',"color:#e0245e");
        $('#likeCount').html(" "+(likeCount+1))
    }
    var id = $('#challenge-id').val();
    CTFd.fetch('/api/v1/challenges/' + id + '/like', {
        method: 'POST'
    }).then(function (response) {
        return response.json();
    }).then(function (response) {
        if (!response.success) {
            ezal({
                title: "Error",
                body: "Failed to like the current challenge",
                button: "Got it!"
            });
        }
    });
}

function loadchals(cb) {
    $.get(script_root + "/api/v1/challenges", function (response) {
        var categories = [];
        var cat;
        challenges = response.data;

        $('#challenges-board').empty();
        $('#button_list').empty();
        $.get(script_root + "/api/v1/category", function (response2) {
        cat = response2.data;
        for (var i = 0; i <= cat.length-1; i++) {
            /*challenges[i].solves = 0;*/
            let name = cat[i].name;
            let description = cat[i].description;
            let id = cat[i].id;
            var categoryTab = "";
            if(i == 0){
                $("#button_list").append($(
                    '<li class="nav-item">'+
                    '<h3 data-toggle="tab" href="#{0}" class="nav-link active" id="{1}" onclick="button=this.id">'.format(name.replaceAll(" ",'')+id.toString(),id)+
                    arrow+
                    ' {0}</a></li>'.format(name)));
                categoryTab = '<div id="{0}" class="tab-pane fade active show">'.format(name.replaceAll(" ",'')+id.toString());
            }else{
                $("#button_list").append($(
                    '<li class="nav-item">'+
                    '<h3 data-toggle="tab" href="#{0}" class="nav-link" id="{1}" onclick="button=this.id">'.format(name.replaceAll(" ",'')+id.toString(),id)+
                    '{0}</a></li>'.format(name)));
                categoryTab = '<div id="{0}" class="tab-pane fade">'.format(name.replaceAll(" ",'')+id.toString());
            }
            //if ($.inArray(name, categories) == -1) {
                var category = name;
                categories.push(category);

                var categoryid = category.replace(/ /g, "-").hashCode();
                var categoryrow = $(
                    categoryTab +
                    '<div id="{0}-row" class="pt-2">'.format(id) +
                    '<div class="category-header col-md-12 mb-4">' +
                    '</div>' +
                    '<div class="category-challenges col-md-12">' +
                    '<div class="challenges-row col-md-12"></div>' +
                    '</div>' +
                    '</div>' + '</div>');
                categoryrow.find(".category-header").append($("<p class='mt-3' style='font-size:1.15rem;color:#37d63e;'>" + description + "</p>"));

                $('#challenges-board').append(categoryrow);
            //}
        }
        for (var i = 0; i <= challenges.length - 1; i++) {
            var chalinfo = challenges[i];
            //var challenge = chalinfo.category.replace(/ /g, "-").hashCode();
            var chalid = chalinfo.name.replace(/ /g, "-").hashCode();
            //var catid = chalinfo.category.replace(/ /g, "-").hashCode();
            var catid = chalinfo.category_id;
            var chalwrap = $("<div id='{0}' class='col-md-3 d-inline-block'></div>".format(chalid));
            if(!chalinfo.lock){
                if (user_solves.indexOf(chalinfo.id) == -1) {
                    var chalbutton = $("<button class='btn btn-dark challenge-button w-100 text-truncate pt-3 pb-3 mb-2' value='{0}'></button>".format(chalinfo.id));
                } else {
                    var chalbutton = $("<button class='btn btn-dark challenge-button solved-challenge w-100 text-truncate pt-3 pb-3 mb-2' value='{0}'><i class='fas fa-check corner-button-check'></i></button>".format(chalinfo.id));
                }

                var chalheader = $("<p>{0}</p>".format(chalinfo.name));
                var chalscore = $("<span>{0}</span>".format(chalinfo.value));
                for (var j = 0; j < chalinfo.tags.length; j++) {
                    var tag = 'tag-' + chalinfo.tags[j].value.replace(/ /g, '-');
                    chalwrap.addClass(tag);
                }

                chalbutton.append(chalheader);
                chalbutton.append(chalscore);
            }else{
                var chalbutton = $("<button class='btn btn-dark challenge-button w-100 text-truncate pt-3 pb-3 mb-2' value='{0}'><i class='fas fa-lock fa-4x'></i></button>".format(chalinfo.id));
            }
            
            chalwrap.append(chalbutton);

            $("#" + catid + "-row").find(".category-challenges > .challenges-row").append(chalwrap);
        }

        $('.challenge-button').click(function (e) {
            loadchal(this.value);
            getsolves(this.value);
        });

        if (cb) {
            cb();
        }
        });
    });
}



$('#submit-key').click(function (e) {
    submitkey($('#challenge-id').val(), $('#submission-input').val(), $('#nonce').val())
});



$('.challenge-solves').click(function (e) {
    getsolves($('#challenge-id').val())
});

$('#challenge-window').on('hide.bs.modal', function (event) {
    $("#submission-input").removeClass("wrong");
    $("#submission-input").removeClass("correct");
    $("#incorrect-key").slideUp();
    $("#correct-key").slideUp();
    $("#already-solved").slideUp();
    $("#too-fast").slideUp();
});

var load_location_hash = function () {
    if (window.location.hash.length > 0) {
        loadchalbyname(decodeURIComponent(window.location.hash.substring(1)));
    }
};

function update(cb) {
    load_user_solves(function () { // Load the user's solved challenge ids
        loadchals(function () { //  Load the full list of challenges
            if (cb) {
                cb();
            }
        });
    });
}

$(function () {
    update(function () {
        load_location_hash();
    });
});

$('.nav-tabs a').click(function (e) {
    e.preventDefault();
    $(this).tab('show')
});

$('#challenge-window').on('hidden.bs.modal', function () {
    $('.nav-tabs a:first').tab('show');
    history.replaceState('', document.title, window.location.pathname);
});

setInterval(update, 300000);
