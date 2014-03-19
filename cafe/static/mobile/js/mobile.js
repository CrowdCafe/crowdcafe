$(document).ready(function(){
	$('.element').click(function(){
		if ($(this).hasClass('checked')){
			$(this).removeClass('checked');
		}else{
			$(this).addClass('checked');
		}
	});
});