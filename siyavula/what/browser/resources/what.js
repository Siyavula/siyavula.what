jq(document).ready(function(){
    
    jq("input#siyavula-what-question-add-button").click(function(event) {
        event.preventDefault();
        text = jq("textarea#question").val();
        if (text == "") {
            alert('You must supply a question.');
            return;
        }
        uuid = jq('input#content_uuid');
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

function displayError(jqXHR, textStatus, errorThrown) {
    alert(textStatus);
    spinner = jq('img#spinner');
    jq(spinner).hide();
}
