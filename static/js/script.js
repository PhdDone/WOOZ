
var firstTaskFinished = false
//version 1.5
//version 1.6 //fix price bug, save do_not_care into db, save original price into db
//version 1.6.1 // fix ajax redirect bug

var version = null;

//https://stackoverflow.com/questions/25025465/tracking-ajax-error-on-readystate-0-status-0-and-statustext-error
//http://bartwullems.blogspot.com.tr/2012/02/ajax-request-returns-status-0.html
$(document).ajaxError(function(e, jqxhr, settings, exception) {
    if (jqxhr.readyState == 0 || jqxhr.status == 0) {
        return; //Skip this error
    }
});

function submitHit() {
    $('#userSubmit').hide()
    var taskId = $('#taskId').text();
    var userResponse = $('#userResponse').val();
    var context = $('#context').html().replace(/(\r\n|\n|\r| |<|>)/gm,"");
    var context = context.replace(/(")/gm,"|");
    $.ajax({
        type: 'POST',
        url: "/userUpdateTask",
        data: JSON.stringify({
            "task_id": taskId,
            "annotation": userResponse,
            "version": version,
            "context": context
        }),
        error: function (e) {
            console.log(e);
        },
        dataType: "json",
        contentType: "application/json",
        success: function (response) {
            alert(JSON.stringify(response))
            console.log(response);
        }
    });
};

function submitUserResponse() {
    $('#userSubmit').hide()
    var taskId = $('#taskId').text();
    var userResponse = $('#userResponse').val();
    var end = $('#endOfDialogue').prop('checked');
    console.log(end)
    $.ajax({
        type: 'POST',
        url: "/userUpdateTask",
        data: JSON.stringify({
            "task_id": taskId,
            "user_response": userResponse,
            "version": version
        }),
        error: function (e) {
            console.log(e);
        },
        dataType: "json",
        contentType: "application/json",
        success: function (response) {
            alert(JSON.stringify(response))
            console.log(response);
        }
    });
};

function searchEditTask() {
    var taskId = $('#taskId').val().trim();
    console.log(taskId)
    $.ajax({
        type: 'POST',
        url: "/searchEditTask",
        data: JSON.stringify({
            "task_id": taskId,
        }),
        error: function (e) {
            console.log(e);
        },
        dataType: "json",
        contentType: "application/json",
        success: function (response) {
                var pretty = JSON.stringify(response, undefined, 4);
                console.log(pretty)
                $('#taskJson').val(pretty)
            alert(JSON.stringify(response))
            console.log(response);
        }
    });
};

function submitEditTask() {
    var taskJson;
    try {
        var taskJsonString = $('#taskJson').val()
        taskJson = JSON.parse(taskJsonString)
    } catch (e) {
        alert("JSON format error")
        return false;
    }
    $.ajax({
        type: 'POST',
        url: "/submitEditTask",
        data: JSON.stringify({
            "task_json": taskJson
        }),
        error: function (e) {
            console.log(e);
        },
        dataType: "json",
        contentType: "application/json",
        success: function (response) {
            var pretty = JSON.stringify(response, undefined, 4);
            console.log(pretty)
            $('#taskJson').val(pretty)
            alert(JSON.stringify(response))
            console.log(response);
        }
    });
};

$(document).ready(function() {
    firstTaskFinished = false
    version = 1.6
    var buttonadd = '<div class="col-xs-2" style="padding: 0;"><button class="btn btn-success btn-add" type="button"><div class="glyphicon glyphicon-plus"></button></div>';
    var fvrhtmlclone = '<div class="fvrclonned col-xs-12">' + $(".fvrduplicate").html() + buttonadd + '</div>';
    $(".fvrduplicate").html(fvrhtmlclone);
    $(".fvrduplicate").after('<div class="fvrclone"></div>');

    var baseHtml = $("#diaact-0").html()
    var counter = 1

    $(document).on('click', '.btn-add', function (e) {
        if ($(this).hasClass('btn-add-2')){
            console.log("2")
        } else {
            //e.preventDefault();
            console.log($(this).parent().parent())
            $(this).parent().parent().parent().append(fvrhtmlclone)
            $(this).removeClass('btn-add').addClass('btn-remove')
                .removeClass('btn-success').addClass('btn-danger')
                .html('<span class="glyphicon glyphicon-minus"></span>');
        }
    }).on('click', '.btn-remove', function (e) {
        $(this).parents('.fvrclonned').remove();
        //e.preventDefault();
        counter--
        //return false;
    });

    $("#AddDiaact").click(function () {
        if (counter > 10) {
            alert("Only 10 dia act is allowed");
            return false;
        }
        var index = counter
        var newDiaactDiv = "<div class='form-group row dup' id='diaact-" + index + "'>" + baseHtml + "</div>"

        //var newTextBoxDiv = $(document.createElement('div'))
         //   .attr("id", 'TextBoxDiv' + counter);

        //newTextBoxDiv.after().html('<label>Textbox #' + counter + ' : </label>' +
        //    '<input type="text" name="textbox' + counter +
        //    '" id="textbox' + counter + '" value="" >');

        //newTextBoxDiv.appendTo("#TextBoxesGroup");
        $('.diaact').append(newDiaactDiv)

        counter++;
        console.log("now we have " + counter)
    });

    $("#RemoveDiaact").click(function () {
        console.log(counter)
        if (counter == 0) {
            alert("No more dialogue act to remove");
            return false;
        }

        var idx = counter - 1
        console.log("removing " + idx)
        $("#diaact-" + idx).remove();
        counter--;

    });
    $("#getButtonValue").click(function () {

        for (var i = 0; i < counter; ++i) {
            var x = $('#diaact-' + i)
            console.log(x)
            var sysSlotNames = $('#diaact-' + i).find('.sysSlotName').map(function () {
                return $(this).val();
            }).get();

            var sysSlotValues = $('#diaact-' + i).find('.sysSlotValue').map(function () {
                return $(this).val();
            }).get();
            console.log(i)
            console.log(sysSlotNames)
            console.log(sysSlotValues)
        }
        var msg = '';
        for (i = 1; i < counter; i++) {
            msg += "\n Textbox #" + i + " : " + $('#textbox' + i).val();
        }
        alert(msg);
    });
});


function showValues() {
    var fields = $( ":input" ).serializeArray();
    $( "#results" ).empty();
    jQuery.each( fields, function( i, field ) {
        $( "#results" ).append( field.value + " " );
    });
}

function test() {
    var sysSlotNames = $(".sysSlotName").map(function () {
        return $(this).val();
    }).get();

    var sysSlotValues = $(".sysSlotValue").map(function () {
        return $(this).val();
    }).get();
    console.log(sysSlotNames)
    console.log(sysSlotValues)
}