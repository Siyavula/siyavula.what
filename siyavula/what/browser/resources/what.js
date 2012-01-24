jq(document).ready(function(){
    
    jq("input#siyavula-what-question-add-button").click(function(event) {
        event.preventDefault();
        text = jq("textarea#question").val();
        if (text == "") {
            alert('You must supply a question.');
            return;
        }
        context_url = jq('input#context_url').attr('value');
        jq.ajax({
            url: context_url + "/@@add-question-json",
            data: {
                'question': text,
            },
            success: updateQuestions,
            error: displayError,
            dataType: "json",
        });
    });

    jq("form#siyavula-add-answer-form").find('button').click(function(event) {
        event.preventDefault();
        text = jq(this).parent().find('textarea').val()
        if (text == "") {
            alert('You must supply an answer.');
            return;
        }
        questionid = jq('input.questionid').val();
        context_url = jq('input#context_url').attr('value');
        jq.ajax({
            url: context_url + "/@@add-answer-json",
            data: {
                'answer': text,
                'questionid': questionid,
            },
            success: updateAnswers,
            error: displayError,
            dataType: "json",
            context: jq(this).parent(),
        });
    });

});

function updateQuestions(data, textStatus, jqXHR) {
    var result = data.result;
    var html = data.html;
    if (result == 'failure') {
        alert(data.message);
        return;
    }
    jq('div#what-container').append(html);
    jq("textarea#question").attr('value', "");
}

function updateAnswers(data, textStatus, jqXHR) {
    var result = data.result;
    var html = data.html;
    if (result == 'failure') {
        alert(data.message);
        return;
    }
    element = jq(this).find('textarea');
    element.before(html);
    element.attr('value', "");
}

function displayError(jqXHR, textStatus, errorThrown) {
    alert(textStatus);
    spinner = jq('img#spinner');
    jq(spinner).hide();
}

