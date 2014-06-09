function Drawing(easel){
	
	this.easel = easel;
	this.easel.drawing = this;
	this.shapes = [];
	this.mousedown = false;
	this.currentType = false;
	this.startPosition = {
		'x':0,
		'y':0
	};

	this.latesttap = new Date().getTime();
	this.even = true;
	this.activeShape = false;
}

Drawing.prototype = {
	createInputHidden : function(form){
		this.shapes.forEach(function(shape){
			shape.createInputHidden(form);
		});
	},
	getLastShape : function(){
		return this.shapes.slice(-1)[0];
	},
	init: function(shapeType){
		var dE = this, 
		canvas = this.easel.canvas;
		this.currentType = shapeType;

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
		var doubleclick = Tactile.checkDouble();
		if (position){
			this.startPosition = position;

			if(doubleclick){
				this.easel.inprocess = true;
				this.mousedown = true;
				
				this.activeShape = new Shape(this,this.currentType);
				this.activeShape.create({
					x:position.x,
					y:position.y,
					rx:10,
					ry:10
				});
			}else{
				this.mousedown = false;
			}
		}
	},
	draw: function(position){
		if (position){
			if (!this.mousedown) {
				return false;
			}else{

				var radius_x = Math.abs(position.x-this.startPosition.x);
				var radius_y = Math.abs(position.y-this.startPosition.y);

				this.activeShape.update({'rx':radius_x,'ry':radius_y});
			}
		}
	},
	finish: function(){
		this.easel.inprocess = false;
		this.mousedown = false;
	}
}