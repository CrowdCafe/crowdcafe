var drawings = []
function Drawing(image){
	drawings.push(this);

	this.shapes = [];
	this.image = image;
	this.container = $$(image).parent();
	this.canvas = this.container.children('.raphael');
	this.svg = this.canvas.children();
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
		this.correctPosition();
		this.correctSize();
	},
	scrolling: function(position){

		if (this.scroll.active) {
			var delta = (this.scroll.start.y - position.y);
			$$('.page-content')[0].scrollTop = this.scroll.top + delta;		
		}
		return false;
	},
	init : function(){
		var drawing = this, mousedown = false;

		drawing.paper = new Raphael(this.canvas[0]);

		drawing.paper.setViewBox(0,0,this.image.width(),this.image.height(),true);
		drawing.paper.setSize('100%', '100%');
		
		drawing.display();
		// Correct position of the SVG canvas as the position is absolute
		$$('.page-content').on('scroll',function(){
			drawing.display();
		});
		// Correct the size of the SVG canvas
		$$(window).on('resize',function(){
			drawing.display();
		});
		drawing.initScrolling();
	},
	initScrolling: function(){
		var drawing = this;

		drawing.container.find('.button-cancel').on('click',function(){
			drawing.paper.top.remove();
		});

		drawing.canvas[0].addEventListener('touchstart',function(e){
			console.log('started '+drawings.indexOf(drawing));

			drawing.scroll.start = Tactile.getPosition(e);

			console.log($$(drawing.canvas[0]).offset());
			drawing.scroll.top = $$('.page-content')[0].scrollTop;
			drawing.scroll.active = true;
		}, false);
		drawing.canvas[0].addEventListener('touchmove',function(e){
			if (!drawing.inprocess) {
				console.log('moving '+drawings.indexOf(drawing));
				drawing.scrolling(Tactile.getPosition(e));
			}
		}, false);
		drawing.canvas[0].addEventListener('touchend',function(e){
			drawings.forEach(function(entry){
				console.log('cancelled');
				entry.scroll.active = false;
				entry.display();
			});
		}, false);
	}
}
