$(document).ready(function(){
	
	// When a list item that contains an unordered list
	// is hovered on
	$("#nav li").has("ul").hover(function(){
		//Add a class of current and fade in the sub-menu
		$(this).addClass("current").children("ul").slideToggle();
	}, function() {

		// On mouse off remove the class of current
		// Stop any sub-menu animation and set its display to none
		$(this).removeClass("current").children("ul").slideToggle();
	});

});
