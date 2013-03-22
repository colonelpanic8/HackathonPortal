$(document).ready(function() {
    $(".edit").click(function(element){
        target = '#'+ element.target.getAttribute('value');
       	$(target).slideToggle();
    }); 

    $(function() {
	var availableTags;
	$.get('/person/get_handles_matching', function(data) {
	    availableTags = JSON.parse(data);
	    $( "#member-input" ).autocomplete({
		source: availableTags
	    });
	});
    });

});

