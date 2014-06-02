function Dot(shape,position){
	this.shape = shape;
	this.shape.dots.push(this);
	var radius = 8;
	var stroke = 2;
	this.radius = radius;
	this.stroke = stroke;

	this.position = position;
	this.position.x = this.position.x - (this.radius);
	this.position.y = this.position.y - (this.radius);

	
	var circle = this.shape.canvas.getContext('2d');

	circle.beginPath();
	circle.arc(this.position.x, this.position.y, this.radius, 0, 2 * Math.PI, false);
	circle.fillStyle = '#FF5E3A';
	circle.fill();
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
Dot.prototype.inArea = function(position){
	var dot = this;
	var magnet = 10;
	if (Math.pow(position.x - dot.position.x,2) + Math.pow(position.y - dot.position.y,2) < Math.pow(dot.radius+dot.stroke + magnet,2))
		return true;
	else
		return false;
}

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
function Shape(canvas){
	this.canvas = canvas;
	this.dots = [];
}
Shape.prototype.getClickedDot = function(position){
	var clickedDot = false;
	var shape = this;
	shape.dots.forEach(function(dot){
		if (dot.inArea(position))
			clickedDot = dot;
	});
	return clickedDot;
}
