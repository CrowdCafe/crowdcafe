// Initialize your app
var myApp = new Framework7();
var APIurl = 'http://localhost:8000/cafe/';

// Add view
var mainView = myApp.addView('.view-main', {
    // Because we use fixed-through navbar we can enable dynamic navbar
    dynamicNavbar: true
});

var jsonprequest = function(extention,callbackfunction,errorfunction){
	$.ajax({
		type : "GET",
		media_type: "application/javascript",
		//charset: "utf-8",
		url : APIurl+extention+"/", // ?callback=?
		success: callbackfunction,
		error: errorfunction
	});
}

$(document).ready(function(){
	jsonprequest('user',
		function(data){
			console.log(data);
		}/*,
		function(){
			window.open(APIurl+'auth/');
		});*/
	);
});

var getTasks = function(){
	jsonprequest('tasks',function(data){
		$.each(data, function(){
			var task_data = this;
			var task = ' <li><a href="pages/task.html" task-id = "'+task_data.id+'" class="item-link item-content task">'+
			'<div class="item-media"></div>'+
			'<div class="item-inner">'+
			'<div class="item-title-row">'+
			'<div class="item-title">'+task_data.title+'</div>'+
			'</div>'+
			'<div class="item-subtitle">'+task_data.description+'</div>'+
			'</div></a>'+
			'</li>';
			$('.task-list').prepend(task);

			$('[task-id='+task_data.id+']').click(function(){
				setTimeout(function(){
					console.log(1);
					getInstances(task_data);
				}, 100);
			})
			console.log('task: ' + task_data);
		});
	});
}

function getInstances(task){
	//console.log(task_handler);
	$('.instance-list').empty();
	$('.task-title').text(task.title);
	$('.task-description').text(task.description);

	jsonprequest("tasks/"+task.id+"/instance",function(data){
		$.each(data.dataitems, function(){
			var instance = '<li class="swipeout" instance-id="'+this.id+'">'+
			'<div class="swipeout-content" style="-webkit-transform: translate3d(0px, 0px, 0px);">'+
			'<a href="#" class="item-link item-content">'+
			'<div class="item-inner">'+
			'<div class="item-title-row">'+
			'<div class="item-title">'+this.value.user.screen_name+'</div>'+
				//'<div class="item-after">{item_additional}</div>'+
				'</div>'+
				//'<div class="item-subtitle">'+snapshot.val().source+'</div>'+
				'<div class="item-text">'+this.value.text+'</div>';
				var image = false;
				if (this.value.entities.media){
					$.each(this.value.entities.media,function(){
						if (this.type == 'photo')
							image = '<img src="'+this.media_url+'" height="200">';
					})
				}
				if (image)
					instance+='<div class="item-text">'+image+'</div>';

				instance += '</div></a></div>'+
				'<div class="swipeout-actions">'+
				'<div class="swipeout-actions-inner">'+
				'<a href="#" class="demo-actions dontknow swipeout-delete" answer="dontknow">?</a>'+
				'<a href="#" class="demo-actions positive swipeout-delete" answer="positive">+</a>'+
				'<a href="#" class="demo-actions neutral swipeout-delete" answer="neutral">~</a>'+
				'<a href="#" class="demo-actions negative swipeout-delete" answer="negative">-</a>'+
				'</div>'+
				'</div>'+
				'</li>';
				$('.instance-list').append(instance);
				
			});
});

}