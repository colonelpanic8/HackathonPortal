$(document).ready(function() {
	$(".edit").click(function(element){
        	target = '#'+ element.target.getAttribute('value');
       		$(target).slideToggle();
  	}); 
});

