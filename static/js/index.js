$("form.translate").submit(function(event){
	event.preventDefault(); // don't refresh page

	var inputs = $(this).serializeArray(); // for some reason, returns an array of objects
	var formObj = {};
	for (var i = 0; i < inputs.length; i++)
		formObj[inputs[i].name] = inputs[i].value;

    formObj.code = formObj.code.split("\n");

    $.post("/translate", formObj, function(response){
        response = response["result"];
        console.log(response);
        if (response[0] == "0"){
            $(".binary").val(response[1].join("\n"));
        }
        else {
            alert(response[1]);
        }
    }).fail(function(jqXHR, textStatus, errorThrown){
        alert([textStatus, errorThrown]);
    });
});