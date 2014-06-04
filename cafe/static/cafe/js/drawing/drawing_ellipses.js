function DrawingEllipse(drawing){
	this.drawing = drawing;
	this.mousedown = false;
	this.startPosition = {
		'x':0,
		'y':0
	};
	this.ellipse = false;
	this.mylatesttap = new Date().getTime();
}

DrawingEllipse.prototype = {
	calculateMousePosition: function(e){
		return {
			'x':e.offsetX,
			'y':e.offsetY
		}
	},
	calculateTouchPosition: function(e){
		e.preventDefault();
		var offset = this.drawing.canvas.offset();
		return {
			'x' : e.touches[0].pageX - offset.left,
			'y' : e.touches[0].pageY - offset.top
		}
	},
	init: function(){

		var drawingEllipse = this;
		// ------------------------------------------------------------------
		// Mouse clicking events
		drawingEllipse.drawing.canvas.on('mousedown',function(e){
			drawingEllipse.start(drawingEllipse.calculateMousePosition(e))
		});
		drawingEllipse.drawing.canvas.on('mousemove',function(e){
			drawingEllipse.draw(drawingEllipse.calculateMousePosition(e));
		});
		drawingEllipse.drawing.canvas.on('mouseup',function(e){
			drawingEllipse.finish()
		});
		// ------------------------------------------------------------------
		// Touch events
		drawingEllipse.drawing.svg.addEventListener('touchstart', function(e){
			drawingEllipse.start(drawingEllipse.calculateTouchPosition(e));
		}, false);
		drawingEllipse.drawing.svg.addEventListener('touchmove',function(e){
			drawingEllipse.draw(drawingEllipse.calculateTouchPosition(e));
		}, false);
		drawingEllipse.drawing.svg.addEventListener('touchend', function(e){
			drawingEllipse.finish();
		}, false);
		// ------------------------------------------------------------------
	},
	start: function(position){
		this.mousedown = true;

		var color = getRandomColor();
		this.ellipse = this.drawing.paper.ellipse(position.x, position.y, 10,10).attr({ stroke: color,'stroke-width':5,fill:color,'fill-opacity':0.5 });
		this.startPosition = position;
	},
	draw: function(position){
		if (!this.mousedown) {
			return;
		}
		var radius_x = Math.abs(position.x-this.startPosition.x);
		var radius_y = Math.abs(position.y-this.startPosition.y);

		this.ellipse.attr({'rx':radius_x,'ry':radius_y});
	},
	finish: function(){
		this.mousedown = false;
	}
}