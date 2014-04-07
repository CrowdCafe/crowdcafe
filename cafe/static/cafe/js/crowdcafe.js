var settings = {
	'urls':{
		'logout':'/user/logout/'
	}
};


var crowdcafe = {
	'events':{
		account : function(){
			alert(1);
			$$('.logout').tap(function(){
				window.location =settings.urls.logout;
			});
		},
		home : function(){
			/*$$('.account-link').tap(function(){
				console.log(this);
				myApp.get($$(this).attr('link'),function(data){
					console.log(data);
					crowdcafe.events.account();
				});
			});*/
		}
	}
};