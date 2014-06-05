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

		var dE = this, 
		canvas = this.drawing.canvas;
		// ------------------------------------------------------------------
		// Mouse clicking events
		canvas[0].addEventListener('mousedown', function(e){
			dE.start(Tactile.getPosition(e, canvas.offset()));
		}, false);
		canvas[0].addEventListener('mousemove',function(e){
			dE.draw(Tactile.getPosition(e, canvas.offset()));
		}, false);
		canvas[0].addEventListener('mouseup', function(e){
			dE.finish();
		}, false);
		// ------------------------------------------------------------------
		// Touch events
		canvas[0].addEventListener('touchstart', function(e){
			dE.start(Tactile.getPosition(e, canvas.offset()));
		}, false);
		canvas[0].addEventListener('touchmove',function(e){
			dE.draw(Tactile.getPosition(e, canvas.offset()));
		}, false);
		canvas[0].addEventListener('touchend', function(e){
			dE.finish();
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