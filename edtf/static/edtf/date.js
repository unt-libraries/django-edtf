$(function(){
    $("#edtfform").validate({
        rules: {
	    date: {
                required: true,
                remote: {
		    url: "/edtf/isValid.json",
                    dataFilter: function(data){
                        var json = JSON.parse(data);
                        if(json.validEDTF === true) {
                            return '"true"';
                        } else {
                            return '"Invalid EDTF date"';
                        }
                    }
                }
            }
        },
        messages: {
            required: "date is required",
            remote: "invalid EDTF date"
        },
        submitHandler: function() {
        },
        success: function(label) {
            label.addClass("valid").text("Valid EDTF date.")
        },
        onkeyup: true
    });
});

jQuery.extend(jQuery.validator.messages, {
    required: "A date is required.",
    remote: "Invalid EDTF date.",
});
