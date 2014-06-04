var drawings = []
function Drawing(image){
	drawings.push(this);
	this.image = image;
	this.container = $$(image).parent();
	this.canvas = this.container.children('.raphael');
	this.svg = this.canvas[0];
	this.paper = false;
	this.scroll = {
		'active':false,
		'top':0,
		'start':{}
	}
	this.inprocess = false;
}

Drawing.prototype = {
	correctSize : function(){
		this.canvas.css('width',this.image.width()+'px');
		this.canvas.css('height',this.image.height()+'px');
	},
	correctPosition : function(){
		var offset = this.image.offset();

		this.canvas.css('left',(offset.left)+'px');
		this.canvas.css('top',(offset.top)+'px');
	},
	display: function(){

		if (!this.scroll.active){
			this.correctPosition();
			this.correctSize();
			this.canvas.show();
		}else{
			this.canvas.hide();
		}
	},
	scrolling: function(position){

		if (this.scroll.active) {
			var delta = (this.scroll.start.y - position.y);
			$$('.page-content')[0].scrollTop = this.scroll.top + delta;		
		}
		return false;
	},
	init : function(){
		var drawing = this;

		drawing.paper = new Raphael(this.svg, this.image.width(), this.image.height()), mousedown = false;
		
		drawing.display();
		// Correct position of the SVG canvas as the position is absolute
		$$('.page-content').on('scroll',function(){
			
			drawing.display();
		});
		// Correct the size of the SVG canvas
		$$(window).on('resize',function(){
			drawing.correctSize();
		});
		drawing.initScrolling();
	},
	initScrolling: function(){
		var drawing = this;

		drawing.container.find('.button-cancel').on('click',function(){
			drawing.paper.top.remove();
		});

		drawing.svg.addEventListener('touchstart',function(e){
			console.log('started '+drawings.indexOf(drawing));
			drawing.scroll.active = true;
			drawing.scroll.start = Tactile.getTouchPosition(e, $$(drawing.svg).offset());
			console.log($$(drawing.svg).offset());
			drawing.scroll.top = $$('.page-content')[0].scrollTop;
		}, false);
		drawing.svg.addEventListener('touchmove',function(e){
			if (!drawing.inprocess) {
				console.log('moving '+drawings.indexOf(drawing));
				drawing.scrolling(Tactile.getTouchPosition(e, $$(drawing.svg).offset()));
			}
		}, false);
		drawing.svg.addEventListener('touchend',function(e){
			drawings.forEach(function(entry){
				console.log('cancelled');
				entry.scroll.active = false;
				entry.display();
			});
		}, false);
	}
}
