// Initialize your app
var crowdcafe = new Framework7({
	dynamicNavbar: true,
	modalTitle: 'CrowdCafe',
	swipeBackPage:false,
	preloadPreviousPage: false,
	cache:false,
	ajaxLinks:false
});
var $$ = Framework7.$;


crowdcafe.swipeoutDelete = function (el) {
            el = $$(el);
            if (el.length === 0) return;
            if (el.length > 1) el = $$(el[0]);
            crowdcafe.swipeoutOpenedEl = undefined;
            el.trigger('delete');
            el.css({height: el.outerHeight() + 'px'});
            var clientLeft = el[0].clientLeft;
            el.css({height: 0 + 'px'}).addClass('deleting transitioning').transitionEnd(function () {
                el.trigger('deleted');
                //el.remove();
            });
            el.find('.swipeout-content').transform('translate3d(-100%,0,0)');
        };
// Add view
var mainView = crowdcafe.addView('.view-main', {
    // Because we use fixed-through navbar we can enable dynamic navbar
    dynamicNavbar: true
});

var page_scripts = {
	task: function(){
		$$('.button-submit').on('click',function(){
			crowdcafe.showPreloader('Saving...');
			document.taskForm.submit();
		});
		$$('.skip-instance').on('click',function(){
			crowdcafe.showPreloader('Skipping...');
		});
		$$('.open-popup').on('click', function(){
			var button = $$(this);
			if (button.attr('iframe')){
				var content = '<iframe src="'+button.attr('iframe')+'" height="'+$$(window).height()+'"></iframe>'
				$$(button.attr('data-popup')+' .content-block').html(content);
			}
		});

		$$('[answer-to]').on('click',function(){
			var answer_button = $$(this);
			var question = {
				'name':answer_button.attr('answer-to'),
				'answer': answer_button.attr('answer')
			};
			console.log(question);
			$$(question.name).val(question.answer);	
			answer_button.parents('.question').removeClass('notanswered').addClass('answered');
			if (answer_button.parents('.hide-if-empty').find('.question.notanswered').length == 0){
				answer_button.parents('.hide-if-empty').hide();
			}
		});

	},
	rewards: function(){
		$$('.get-reward').on('click',function(){
			crowdcafe.confirm('Do you really want to get this reward?', function () {
				crowdcafe.alert('Great!');
			});
		});
	},
	tasklist: function(){
		$$('.task').on('click',function(){
			crowdcafe.showPreloader()
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