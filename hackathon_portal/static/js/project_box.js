$(document).ready(function() {
	$('.project-box').each(function(index, element) {
		new window.hackathonPortal.ProjectBox($(element));	
	});
});

window.hackathonPortal = {};

window.hackathonPortal.ProjectBox = function(container) {
	this.container= container;
	var projectBox = this;
	this.moreInfo = this.container.find('.more-info');
	this.container.hover(
		function() {
			projectBox.showMoreInfo()
	},
		function(){
			projectBox.hideMoreInfo()
	});	
};

window.hackathonPortal.ProjectBox.prototype.showMoreInfo = function() {
	if (this.currentHeight === undefined) {
		this.currentHeight = this.moreInfo.height();
	}
	this.moreInfo.height('0').show();
	this.moreInfo.stop().animate({'height': this.currentHeight}, 500);
};

window.hackathonPortal.ProjectBox.prototype.hideMoreInfo = function() {
	this.moreInfo.stop().animate({'height': '0'}, 500);
};
