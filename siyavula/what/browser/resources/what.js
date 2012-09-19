// WARNING:
// The js here can be overridden in any of the products that use the
// siyavula.what. If you don't see the js here executing, double check
// the other products/layers for overridding scripts. Grep is your friend :)

jq(document).bind('loadInsideOverlay', function() {

    jq('textarea.mce_editable').each(function() {
        var config_id = $(this).attr('id');
        delete InitializedTinyMCEInstances[config_id];
        var config = new TinyMCEConfig(config_id);
        config.init();
    });

    jq("div#answer-action-buttons-container button.siyavula-add-answer-button")
        .click(function(event) {
        event.preventDefault();
        var answerid = jq(this).attr('answerid');
        var editor = jq('iframe#answer_ifr').contents().find('body');
        var contents = jq(editor).html();
        if (contents == "<p><br mce_bogus=\"1\"></p>" || contents == '') {
            alert('You must supply an answer.');
            return;
        }
        var answerform = jq(this).parent().parent();
        var questionid = jq(answerform).find('input.questionid').val();
        context_url = jq(this).attr('context_url');
        jq('.close').click();
        pb.spinner.show();
        jq.ajax({
            url: context_url + "/@@add-answer-json",
            data: {
                'answer': contents,
                'questionid': questionid
            },
            success: updateAnswers,
            error: displayError,
            dataType: "json",
            context: answerform
        });
    });
    
}); 

jq(document).ready(function(){
    
    jq("input#siyavula-what-question-add-button").click(function(event) {
        event.preventDefault();
        text = jq("textarea#question").val();
        if (text == "") {
            alert('You must supply a question.');
            return;
        }
        context_url = jq(this).attr('context_url');
        jq.ajax({
            url: context_url + "/@@add-question-json",
            data: {
                'question': text
            },
            success: updateQuestions,
            error: displayError,
            dataType: "json"
        });
    });

    jq("button.siyavula-add-answer-button").prepOverlay({
        subtype: 'ajax',
        filter: '#content',
        closeselector: '[name=form.button.cancel]',
        api: true
    });

    jq("form[name='delete-question']")
        .find("input[name='action.button']").click(deleteQuestion);
        
    jq("form[name='delete-answer']")
        .find("input[name='action.button']").click(deleteAnswer);
});

function deleteAnswer(event) {
    event.preventDefault();
    questionid = jq(this).parent().find('input[name="questionid"]').val();
    answerid = jq(this).parent().find('input[name="answerid"]').val();
    context_url = jq(this).attr('context_url');
    jq.ajax({
        url: context_url + "/@@delete-answer-json",
        data: {
            'questionid': questionid,
            'answerid': answerid
        },
        success: removeAnswer,
        error: displayError,
        dataType: "json"
    });
}

function deleteQuestion(event) {
    event.preventDefault();
    questionid = jq(this).parent().find('input[name="questionid"]').val();
    context_url = jq(this).attr('context_url');
    jq.ajax({
        url: context_url + "/@@delete-question-json",
        data: {
            'questionid': questionid
        },
        success: removeQuestion,
        error: displayError,
        dataType: "json"
    });
}

function removeQuestion(data, textStatus, jqXHR) {
    var result = data.result;
    if (result == 'failure') {
        alert(data.message);
        return;
    }
    element = jq('div#'+data.questionid).remove();
}

function updateQuestions(data, textStatus, jqXHR) {
    var result = data.result;
    var html = data.html;
    if (result == 'failure') {
        alert(data.message);
        return;
    }
    jq('div#what-container').append(html);
    jq("textarea#question").attr('value', "");

    // find delete button in returned html
    var container = jq('div#' + data.questionid +"'");
    var button = jq(container).find('input@[name="action.button"]');
    // add delete click eventhandler
    jq(button).bind('click', deleteQuestion);
}

function updateAnswers(data, textStatus, jqXHR) {
    pb.spinner.hide();

    var result = data.result;
    var html = data.html;
    if (result == 'failure') {
        alert(data.message);
        return;
    }
    questionid = jq(this).find('.questionid').attr('value');
    element = jq(document).find('div#' + questionid + '-answers-list');
    element.append(html);
    button = jq('div#'+data.answerid).find('input@[name="action.button"]');
    jq(button).bind('click', deleteAnswer);
    jq('div#' + questionid + ' label').show();
}

function removeAnswer(data, textStatus, jqXHR) {
    var result = data.result;
    if (result == 'failure') {
        alert(data.message);
        return;
    }
    element = jq('div#'+data.answerid);
    container = jq(element).parent().parent();
    jq(element).remove();
    answers = jq(container).find('div.answer');
    if (answers.length < 1) {
        jq(container).find('label').hide();
    }
}

function displayError(jqXHR, textStatus, errorThrown) {
    alert(errorThrown);
    spinner = jq('img#spinner');
    jq(spinner).hide();
}

