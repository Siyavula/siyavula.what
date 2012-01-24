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
        text = jq(this).parent().find('textarea').val();
        if (text == "") {
            alert('You must supply an answer.');
            return;
        }
        questionid = jq(this).parent().find('input.questionid').val();
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
    
    jq("form[name='delete-question']")
        .find("input[name='action.button']").click(function(event) {

        event.preventDefault();
        questionid = jq(this).parent().find('input[name="questionid"]').val();
        context_url = jq('input#context_url').attr('value');
        jq.ajax({
            url: context_url + "/@@delete-question-json",
            data: {
                'questionid': questionid,
            },
            success: removeQuestion,
            error: displayError,
            dataType: "json",
        });
    });

    jq("form[name='delete-answer']")
        .find("input[name='action.button']").click(function(event) {

        event.preventDefault();
        questionid = jq(this).parent().find('input[name="questionid"]').val();
        answerid = jq(this).parent().find('input[name="answerid"]').val();
        context_url = jq('input#context_url').attr('value');
        jq.ajax({
            url: context_url + "/@@delete-answer-json",
            data: {
                'questionid': questionid,
                'answerid': answerid,
            },
            success: removeAnswer,
            error: displayError,
            dataType: "json",
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

function removeQuestion(data, textStatus, jqXHR) {
    var result = data.result;
    if (result == 'failure') {
        alert(data.message);
        return;
    }
    element = jq('div#'+data.questionid).remove();
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

function removeAnswer(data, textStatus, jqXHR) {
    var result = data.result;
    if (result == 'failure') {
        alert(data.message);
        return;
    }
    element = jq('div#'+data.answerid).remove();
}

function displayError(jqXHR, textStatus, errorThrown) {
    alert(textStatus);
    spinner = jq('img#spinner');
    jq(spinner).hide();
}

