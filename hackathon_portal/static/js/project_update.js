$(document).ready(function() {
	$(".edit").click(function(element){
        	target = '#'+ element.target.getAttribute('value');
       		$(target).slideToggle();
  	}); 

	$(function() {
		var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion",
      "Erlang",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme"
    	];
		$( "#member-input" ).autocomplete({
			source: availableTags
		});
	});
});

