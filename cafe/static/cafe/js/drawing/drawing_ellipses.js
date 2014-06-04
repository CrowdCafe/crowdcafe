function DrawingEllipse(drawing){
	this.drawing = drawing;
	this.mousedown = false;
	this.startPosition = {
		'x':0,
		'y':0
	};

	this.ellipse = false;
	this.latesttap = new Date().getTime();
	this.even = true;
}

DrawingEllipse.prototype = {
	
	init: function(){

		var drawingEllipse = this;
		// ------------------------------------------------------------------
		// Mouse clicking events
		/*drawingEllipse.drawing.canvas.on('mousedown',function(e){
			drawingEllipse.start(drawingEllipse.calculateMousePosition(e))
		});
		drawingEllipse.drawing.canvas.on('mousemove',function(e){
			drawingEllipse.draw(drawingEllipse.calculateMousePosition(e));
		});
		drawingEllipse.drawing.canvas.on('mouseup',function(e){
			drawingEllipse.finish()
		});*/
		// ------------------------------------------------------------------
		// Touch events
		drawingEllipse.drawing.svg.addEventListener('touchstart', function(e){
			drawingEllipse.start(Tactile.getTouchPosition(e, drawingEllipse.drawing.canvas));
		}, false);
		drawingEllipse.drawing.svg.addEventListener('touchmove',function(e){
			drawingEllipse.draw(Tactile.getTouchPosition(e, drawingEllipse.drawing.canvas));
		}, false);
		drawingEllipse.drawing.svg.addEventListener('touchend', function(e){
			drawingEllipse.finish();
		}, false);
		// ------------------------------------------------------------------
	},
	
	start: function(position){
		var now = new Date().getTime();
		var timesince = now - this.mylatesttap;

		this.startPosition = position;
		this.mylatesttap = now;
	
		if((timesince < 400) && (timesince > 0)){
			this.drawing.inprocess = true;
			this.mousedown = true;
			var color = getRandomColor();
			this.ellipse = this.drawing.paper.ellipse(position.x, position.y, 10,10).attr({ stroke: color,'stroke-width':5,fill:color,'fill-opacity':0.5 });
		}else{
			this.mousedown = false;
			
		}

	},
	draw: function(position){
	
		if (!this.mousedown) {
			return false;
		}else{
			
			var radius_x = Math.abs(position.x-this.startPosition.x);
			var radius_y = Math.abs(position.y-this.startPosition.y);
			this.ellipse.attr({'rx':radius_x,'ry':radius_y});
		}
	},
	finish: function(){
		this.drawing.inprocess = false;
		this.mousedown = false;
	}
}