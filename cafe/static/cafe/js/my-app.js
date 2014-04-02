// Initialize your app
var myApp = new Framework7({
	swipeBackPage:false,
	preloadPreviousPage: false,
	cache:false,
	ajaxLinks:false
});
var APIurl = 'http://localhost:8000/cafe/';

// Add view
var mainView = myApp.addView('.view-main', {
    // Because we use fixed-through navbar we can enable dynamic navbar
    dynamicNavbar: true
});