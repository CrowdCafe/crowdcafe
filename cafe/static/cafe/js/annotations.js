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

	$$(canvas).on('mouseup',function () {
		mousedown = false;
	});

	$$(canvas)[0].addEventListener('touchstart', function(event) {
		event.preventDefault();
		block1.className = 'touched';
		block1.innerHTML = 'touched';
	}, false);

	$$(canvas)[0].addEventListener('touchmove', function(event) {
		var x = event.touches[0].pageX;
		var y = event.touches[0].pageY;
		block1.style.left = x - 100;
		block1.style.top = y - 50;
		block1.innerHTML = 'touchmove' + x + '=' + y;
	}, false);

	$$(canvas)[0].addEventListener('touchend', function(event) {
		event.preventDefault();
		block1.className = '';
		block1.innerHTML = 'dropped';
	}, false);


}


