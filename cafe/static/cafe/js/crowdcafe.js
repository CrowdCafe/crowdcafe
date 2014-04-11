// Initialize your app
var crowdcafe = new Framework7({
	modalTitle: 'CrowdCafe',
	swipeBackPage:false,
	preloadPreviousPage: false,
	cache:false,
	ajaxLinks:false
});
var $$ = Framework7.$;
// Add view
var mainView = crowdcafe.addView('.view-main', {
    // Because we use fixed-through navbar we can enable dynamic navbar
    dynamicNavbar: true
});

var page_scripts = {
	task: function(){
		$$('.button-submit').on('click',function(){
			document.taskForm.submit();
		});
		$$('.open-popup').on('click', function(){
			var button = $$(this);
			if (button.attr('iframe')){
				var content = '<iframe src="'+button.attr('iframe')+'" height="'+$$(window).height()+'"></iframe>'
				$$(button.attr('data-popup')+' .content-block').html(content);
			}
		});
	},
	rewards: function(){
		$$('.get-reward').on('click',function(){
			crowdcafe.confirm('Do you really want to get this reward?', function () {
				crowdcafe.alert('Great!');
			});
		});
	}
}

$$(document).on('pageInit', function (e) {
	var page = e.detail.page;
	if (page_scripts[page.name]){
		page_scripts[page.name]();
	}
});



var page_name = $$('.page').attr('data-page');
if (page_scripts[page_name]){
	page_scripts[page_name]();
}