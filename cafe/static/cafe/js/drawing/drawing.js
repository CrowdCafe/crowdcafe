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
	getLastShape : function(){
		return this.shapes.slice(-1)[0];
	},
	init: function(shapeType){
		var dE = this, 
		canvas = this.easel.canvas;
		var container = this.easel.canvas.parent();
		this.currentType = shapeType;

		// ------------------------------------------------------------------
		// Mouse clicking events
		container[0].addEventListener('mousedown', function(e){
			dE.start(Tactile.getPosition(e, container.offset()));
		}, false);
		//container[0].addEventListener('mousemove',function(e){
		//	dE.draw(Tactile.getPosition(e, container.offset()));
		//}, false);
container[0].addEventListener('mouseup', function(e){
	dE.finish();
}, false);

		// ------------------------------------------------------------------
		// Touch events
		container[0].addEventListener('touchstart', function(e){
			dE.start(Tactile.getPosition(e, container.offset()));
		}, false);
		//container[0].addEventListener('touchmove',function(e){
		//	dE.draw(Tactile.getPosition(e, container.offset()));
		//}, false);
container[0].addEventListener('touchend', function(e){
	dE.finish();
}, false);
		// ------------------------------------------------------------------
	},
	start: function(position){
		var doubleclick = Tactile.checkDouble();
		if (position){
			this.startPosition = position;

			if(doubleclick){
				if (!this.activeShape){
					this.easel.imageBackground.opacity = 0.5;
					this.easel.fabric.renderAll();

					this.easel.inprocess = true;
					this.mousedown = true;

					this.activeShape = new Shape(this,this.currentType);
					this.activeShape.create({
						x:position.x,
						y:position.y
					});
				}
				else{
					this.easel.buttons.finish.click();
				}
			}else{
				if (this.activeShape){
					this.activeShape.update({'x':position.x,'y':position.y});
				}
				this.mousedown = false;
			}
		}
		this.easel.fabric.renderAll();
	},
	draw: function(position){
		if (position){
			if (!this.mousedown) {
				return false;
			}else{

				var distance_x = Math.abs(position.x-this.startPosition.x);
				var distance_y = Math.abs(position.y-this.startPosition.y);

				this.activeShape.update({'x':distance_x,'y':distance_y});
			}
			
		}
		this.easel.fabric.renderAll();
	},
	finish: function(){
		this.easel.inprocess = false;
		this.mousedown = false;
		
	}
}