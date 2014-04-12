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
	welcome: function(){
		$$('.external').on('click',function(){
			crowdcafe.showPreloader('redirecting...');
		});
	},
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
			$$(question.name).val(question.answer);	
			answer_button.parents('.question').removeClass('notanswered').addClass('answered');
			if (answer_button.parents('.hide-if-empty').find('.question.notanswered').length == 0){
				answer_button.parents('.hide-if-empty').hide();
			}
		});

	},
	index: function(){
		$$('.tasks-cappuccino,.tasks-wine').on('click',function(){
			crowdcafe.alert('We do not have any tasks from this category available now. Please try "Caffè" tasks now.');
		});
	},
	rewards: function(){
		$$('.get-reward').on('click',function(){
			var reward = {
				'title':$$(this).find('.item-title').text(),
				'cost':$$(this).find('.money').text(),
				'purchase_url':$$(this).attr('purchase-url')
			};
			crowdcafe.confirm('Activate '+reward.title+' for '+reward.cost+' ?', function () {
				console.log(reward.purchase_url);
				//window.location = '/'+reward.purchase_url
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