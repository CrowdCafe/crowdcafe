var shapes = [];
var active_shape = false;
function putTogetherPosition(canvas,image){
	var offset = image.offset();

	canvas.css('top',offset.top+'px');
	canvas.css('left',offset.left+'px');

}
function putTogetherRaphaelPosition(image){
	var svg = $$(image).parent().children('svg');
	var offset = image.offset();
	svg.css('left',offset.left);
	svg.css('top',offset.top);
}
function putTogetherRaphaelSize(image){
	var svg = $$(image).parent().children('svg');

	svg.attr('width',image.width());
	svg.attr('height',image.height());
}
function putTogetherSize(canvas,image){
	canvas.attr('width',image.width());
	canvas.attr('height',image.height());
}

function prepareRaphaelPaper(image){
	var annotation_name = image.attr('annotation-name');
	var offset = image.offset();
	console.log(offset);
	var paper = Raphael(offset.left, offset.top, image.width(), image.height());

	$$('body').children('svg').insertAfter(image);
	var circle = paper.circle(50, 40, 10);
	circle.attr("fill", "#f00");
	circle.attr("stroke", "#fff");

	$$('.page-content').on('scroll',function(){
		putTogetherRaphaelPosition(image);
	});
	$$(window).on('resize',function(){
		putTogetherRaphaelSize(image);
	});

	circle.mousedown(function(e){
		console.log(e);
		circle.attr('x',e.pageX);
		circle.attr('y',e.pageY);
	});
}
function prepareCanvas(image){
	var annotation_name = image.attr('annotation-name');

	$$('body').append('<canvas id ="'+annotation_name+'" name="'+annotation_name+'" ></canvas>');

	var canvas = $$('[name='+annotation_name+']');

	canvas.insertAfter(image);
	initAnnotation(canvas,image);
}
function initAnnotation(canvas,image){
	putTogetherSize(canvas,image);
	putTogetherPosition(canvas,image);
	$$('.page-content').on('scroll',function(){
		putTogetherPosition(canvas,image);
	});
	$$(window).on('resize',function(){
		putTogetherSize(canvas,image);
	});
	var active_shape = false;

	canvas.on('click',function(event){
		var offset = canvas.offset();
		var position = {
			'x':event.x - offset.left,
			'y':event.y - offset.top
		};
		if (!active_shape){
			active_shape = new Shape(canvas[0]);
		}

		var clickedDot = active_shape.getClickedDot(position);
		//console.log(clickedDot);

		if (clickedDot){
			if (clickedDot.i == 0){
				var edge = new Edge(active_shape.dots[active_shape.dots.length - 1],active_shape.dots[0]);
				active_shape = false;
			}
		}else{
			var dot = new Dot(active_shape,position);
			dot.addDom($$('[name=taskForm]'));

		}
	});
}

//--------------------------------------------------------------
function Dot(shape,position){
	this.shape = shape;
	this.shape.dots.push(this);

	var radius = 6;
	var stroke = 3;
	this.radius = radius;
	this.stroke = stroke;

	this.position = position;
	this.position.x = this.position.x - (this.radius);
	this.position.y = this.position.y - (this.radius);


	var circle = this.shape.canvas.getContext('2d');

	circle.beginPath();
	circle.arc(this.position.x, this.position.y, this.radius, 0, 2 * Math.PI, false);
	circle.lineWidth = this.stroke;
	circle.strokeStyle = '#FF9500';
	circle.stroke();

	this.i = this.shape.dots.indexOf(this);
	if (this.i > 0){
		var dot1 = this;
		var dot2 = this.shape.dots[this.i - 1];

		var edge = new Edge(dot1,dot2);
	}
}
Dot.prototype = {
	inArea : function(position){
		var dot = this;
		var magnet = 10;
		if (Math.pow(position.x - dot.position.x,2) + Math.pow(position.y - dot.position.y,2) < Math.pow(dot.radius+dot.stroke + magnet,2)){
			return true;
		}
		else{
			return false;
		}
	},
	addDom : function(parent){
		this.dom = this.shape.name+'_'+this.i;
		var dom = '<input type = "hidden" name="'+this.dom+'" value="'+this.position.x+';'+this.position.y+'">';
		$$(parent).append(dom);
	}
}
//--------------------------------------------------------------
function Edge(dot1,dot2){
	this.dot1 = dot1;
	dot1.outline = this;

	this.dot2 = dot2;
	dot2.inline = this;

	var line = this.dot1.shape.canvas.getContext('2d');

	line.beginPath();
	line.moveTo(this.dot1.position.x,this.dot1.position.y);
	line.lineTo(this.dot2.position.x,this.dot2.position.y);
	line.closePath();
	line.stroke();
}
//--------------------------------------------------------------
function Shape(canvas){
	shapes.push(this);
	this.canvas = canvas;
	this.name = $$(canvas).attr('name')+'_'+shapes.indexOf(this);
	this.dots = [];
}
Shape.prototype = {
	getClickedDot : function(position){
		var clickedDot = false;
		var shape = this;
		shape.dots.forEach(function(dot){
			if (dot.inArea(position))
				clickedDot = dot;
		});
		return clickedDot;
	},
	serialize : function(){
		var serialized = [];
		this.dots.forEach(function(dot){
			serialized.push(dot.position);
		});
		console.log(serialized);
	}
}
//--------------------------------------------------------------



