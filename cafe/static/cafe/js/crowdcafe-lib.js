var $$ = Framework7.$;
var background_classes = ['positive','negative','neutral','gold','dontknow'];

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
		
		$$('.swipeout-actions a').on('click',function(){
			var button = $$(this);
			button.parents('.swipeout').removeClass('swipeout-opened');
			button.parents('.swipeout').find('.swipeout-content').attr('style','');

			var apply_border_to = button.parents('.swipeout').find('.swipeout-content');

			background_classes.forEach(function(entry){
				if (button.hasClass(entry)){
					$$(apply_border_to).addClass('border-'+entry);
				}else{
					$$(apply_border_to).removeClass('border-'+entry);
				}
			});
		});
		$$('[annotation-type=shapes]').each(function(){
			var image = $$(this);
			console.log(image.height());
			
			if (image.height() > 10){
				console.log('image already loaded');
				prepareCanvas(image);
			}else{
				image[0].onload = function(){
					console.log('image loaded');
					prepareCanvas(image);
				};
			}
			
			


		});
		$$('.contexts').on('change',function(){
			var context = $$(this).val();
			crowdcafe.get('/cafe/context/set/?context='+context,function(data){
				console.log(data);
			});
		});
		$$('[value-to-text]').on('change',function(){
			var value_button = $$(this);
			var to_item = {
				'selector':value_button.attr('value-to-text'),
				'value': value_button.val()
			};
			$$(to_item.selector).text(to_item.value);

		});
		$$('[value-to-val]').on('change',function(){
			var value_button = $$(this);
			var to_item = {
				'selector':value_button.attr('value-to-val'),
				'value': value_button.val()
			};
			$$(to_item.selector).val(to_item.value);
			
		});

		$$('[name]').on('change',function(){
			console.log('quality check');
			var field = $$(this);
			var value = (field.val()) ? (field.val()) : field.text();
			qualityCheck($$(this),value);
		});

		$$('[photobrowser-images]').on('click',function(){
			var images_array_string = $$(this).attr('photobrowser-images');
			var splitter = $$(this).attr('photobrowser-splitter');
			var images = images_array_string.split(splitter);

			var photoBrowserPopup = crowdcafe.photoBrowser({
				photos: images,
				type: 'popup'
			});
			photoBrowserPopup.open();
			console.log(images_array_string);
		});

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
				el.remove();
			});
			el.addClass('deleting transitioning');
			el.find('.swipeout-content').transform('translate3d(0,0,0)');

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

			qualityCheck($$(question.name),question.answer);
			answer_button.parents('.question').removeClass('notanswered').addClass('answered');
			//qualityCheck($$(question.name),question.answer);

			setTimeout(function(){
				if (answer_button.parents('.hide-if-empty').find('.question.notanswered').length == 0){
					answer_button.parents('.hide-if-empty').css({display: 'none'}).addClass('transitioning');
				}
			}, 350);


		});

	},
	index: function(){
		page_scripts_activated['index']=true;
		$$('.contexts').on('change',function(){
			var context = $$(this).val();
			crowdcafe.get('/cafe/context/set/?context='+context,function(data){
				console.log(data)
			});
		});
	},
	rewards: function(){
		page_scripts_activated['rewards']=true;

		$$('.external').on('click',function(){
			crowdcafe.showPreloader();
		});

		$$('.coupon a').on('click',function(){
			var button = $$(this);
			$$(button.attr('data-popup')+' .popup-title').html(button.attr('reward-title'));
			var content = '<h1 class="center">Number '+button.attr('reward-index')+'<br/> code: '+button.attr('reward-code')+'</h1><p class="center">'+button.attr('reward-description')+'</p><h4 class="center">'+button.attr('reward-vendor')+'</h4>';
			$$(button.attr('data-popup')+' .popup-content').html(content);
		});

	},
	tasklist: function(){
		page_scripts_activated['tasklist']=true;

		$$('.task').on('click',function(){
			crowdcafe.showPreloader()
		});

	},
	smart_select: function(){
		//to be removed
	}
}

function qualityCheck(element, value){
	console.log('quality check initiated');
	var gold = $$(element).attr('gold'),
	feedback = $$(element).attr('feedback');
	if (gold){
		if (!feedback){
			feedback = 'It should be: '+gold;
		}
		if (gold == value){
			feedback = 'Correct. '+feedback;
			crowdcafe.alert(feedback);
		}else{
			crowdcafe.actions(
				[
				{
					text: '"'+value+'" is incorrect. The right answer is "'+gold+'". '+ feedback,
					label: true
				},

				{
					text: 'Ok, I understand.',
				},

				{
					text: 'I dot not agree. Leave comment to requestor.',
					red: true,
					onClick: function () {
						$$('.instructions-open').trigger('click');
					}
				},
				]
				);
			feedback = 'It is not correct. '+feedback;
		}

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