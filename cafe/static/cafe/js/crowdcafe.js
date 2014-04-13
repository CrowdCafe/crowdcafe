// Initialize your app
var crowdcafe = new Framework7({
	dynamicNavbar: true,
	modalTitle: 'CrowdCafe',
	swipeBackPage:false,
	preloadPreviousPage: true,
	cache:true,
	ajaxLinks:false
});


// Add view
var mainView = crowdcafe.addView('.view-main', {
    // Because we use fixed-through navbar we can enable dynamic navbar
    dynamicNavbar: true
});




$$(document).on('pageInit', function (e) {
	var page = e.detail.page;
	if (page_scripts[page.name] && !page_scripts_activated[page.name]){
		page_scripts[page.name]();
	}
});

var page_name = $$('.page').attr('data-page');
if (page_scripts[page_name] && !page_scripts_activated[page_name]){
	page_scripts[page_name]();
}

