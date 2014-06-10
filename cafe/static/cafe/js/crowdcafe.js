var crowdcafe,mainView;
var $$;


document.addEventListener('DOMContentLoaded', function(){
	$$ = Framework7.$;
	crowdcafe = new Framework7({
		pushState:true,
		dynamicNavbar: true,
		modalTitle: 'CrowdCafe',
		swipeBackPage:false,
		preloadPreviousPage: true,
		cache:true,
		ajaxLinks:false
	});
	// Add view
	mainView = crowdcafe.addView('.view-main', {
		dynamicNavbar: true
	});

	$$(document).on('pageInit', function (e) {
		var page = e.detail.page;
		console.log(page.name);
		if (page_scripts[page.name] && !page_scripts_activated[page.name]){
			console.log('activated');
			page_scripts[page.name]();
		}
		if (page.name.indexOf('smart-select-radio') == 0){
			page_scripts['smart_select']();
		}
	});

	var page_name = $$('.page').attr('data-page');


	if (page_scripts[page_name] && !page_scripts_activated[page_name]){
		page_scripts[page_name]();
	}
});



