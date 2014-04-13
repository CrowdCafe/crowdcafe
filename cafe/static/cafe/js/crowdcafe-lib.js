var $$ = Framework7.$;

function getURLParameter(name) {
	var regexS = "[\\?&]" + name + "=([^&#]*)";
	var regex = new RegExp(regexS);
	var tmpURL = window.location.href;
	var results = regex.exec(tmpURL);
	if (results == null)
		return null;
	return results[1];
}
var page_scripts_activated = {}

var page_scripts = {
	welcome: function(){
		page_scripts_activated['welcome']=true;

		$$('.external').on('click',function(){
			crowdcafe.showPreloader('redirecting...');
		});
	},
	task: function(){
		
		page_scripts_activated['task']=true;

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
		
		if (getURLParameter('completed_previous') == '0'){
			$$('.instructions-open').trigger('click');
		}
		$$('.button-submit').on('click',function(){
			if (allFieldsAreFilled()){
				crowdcafe.showPreloader('Saving...');
				document.taskForm.submit();
			}else{
				crowdcafe.alert('Not all fields are filled. Check carefully.');
			}
		});
		$$('.skip-instance').on('click',function(){
			crowdcafe.showPreloader('shuffle...');
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
		page_scripts_activated['index']=true;

		$$('.tasks-cappuccino,.tasks-wine').on('click',function(){
			crowdcafe.alert('We do not have any tasks from this category available now. Please try "Caffè" tasks now.');
		});
	},
	rewards: function(){
		page_scripts_activated['rewards']=true;

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
		page_scripts_activated['tasklist']=true;

		$$('.task').on('click',function(){
			crowdcafe.showPreloader()
		});
	}
}


function allFieldsAreFilled(){
	var correct = true; 
	$$('[name]').each(function(){

		if (!$$(this).val() && $$(this).attr('name').indexOf("dataitem") > -1){
			correct = false;
		}
	});
	return correct;
}


		/*$$('.open-popup').on('click', function(){
			var button = $$(this);
			if (button.attr('iframe')){
				var content = '<iframe src="'+button.attr('iframe')+'" height="'+$$(window).height()+'"></iframe>'
				$$(button.attr('data-popup')+' .content-block').html(content);
			}
		});*/