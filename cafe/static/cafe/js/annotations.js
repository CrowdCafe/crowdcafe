var shapes = [];
var active_shape = false;

function putTogetherRaphaelSize(image){
	var canvas = svg(image);

	canvas.attr('width',image.width());
	canvas.attr('height',image.height());
}
function putTogetherRaphaelPosition(image){
	var canvas = svg(image);

	var offset = image.offset();
	console.log(canvas);

	canvas.css('left',offset.left+'px');
	canvas.css('top',offset.top+'px');
}
function svg(image){
	return $$(image).parent().children('.raphael');
}
function prepareRaphaelPaper(image){
	var canvas = svg(image)[0],
	paper = new Raphael(canvas, image.width(), image.height()),mousedown = false;

	putTogetherRaphaelSize(image);
	putTogetherRaphaelPosition(image);

	$$('.page-content').on('scroll',function(){
		putTogetherRaphaelPosition(image);
	});
	$$(window).on('resize',function(){
		putTogetherRaphaelSize(image);
	});
	$$(image).parent().find('.button-cancel').on('click',function(){
		paper.top.remove();
	});

	initEllipseDrawing(canvas,paper);
}
function initEllipseDrawing(canvas,paper){
	var mousedown = false,lastX, lastY, path, pathString, ellipse;

	$$(canvas).on('mousedown',function (e) {
		$$('.page-content').prepend('<span>mousedown</span><br/>');
		e.preventDefault();
		mousedown = true;

		var x = e.offsetX,
		y = e.offsetY;
		var color = getRandomColor();
		ellipse = paper.ellipse(x, y, 10,10).attr({ stroke: color,'stroke-width':5,fill:color,'fill-opacity':0.5 });

		lastX = x;
		lastY = y;
	});

	$$(canvas).on('mousemove',function (e) {
		$$('.page-content').prepend('<span>mousemove</span>');
		e.preventDefault();
		if (!mousedown) {
			return;
		}

		var x = e.offsetX,
		y = e.offsetY;
		var radius_x = Math.abs(x-lastX);
		var radius_y = Math.abs(y-lastY);

		ellipse.attr({'rx':radius_x,'ry':radius_y});
	});

	$$(canvas).on('mouseup',function (e) {
		$$('.page-content').prepend('<br/><br/><span>mouseup</span>');
		mousedown = false;
	});

	$$(canvas)[0].addEventListener('touchstart', function(e) {
		e.preventDefault();
		$$('.page-content').prepend('<span>touchstart</span><br/>');
		mousedown = true;

		var x = e.offsetX,
		y = e.offsetY;
		var color = getRandomColor();
		ellipse = paper.ellipse(x, y, 10,10).attr({ stroke: color,'stroke-width':5,fill:color,'fill-opacity':0.5 });

		lastX = x;
		lastY = y;
	}, false);

	$$(canvas)[0].addEventListener('touchmove', function(e) {
		e.preventDefault();
		$$('.page-content').prepend(radius_y+ ' ');
		if (!mousedown) {
			return;
		}
		console.log(e);
		var x = e.targetTouches[0].clientX,
		y = e.targetTouches[0].clientY;
		var radius_x = Math.abs(x-lastX);
		var radius_y = Math.abs(y-lastY);

		ellipse.attr({'rx':radius_x,'ry':radius_y});
	}, false);

	$$(canvas)[0].addEventListener('touchend', function(e) {
		e.preventDefault();
		$$('.page-content').prepend('<br/><br/><span>touchend</span>');
		mousedown = false;
	}, false);


}


