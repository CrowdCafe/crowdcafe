var easels = []

function Easel(image,namespace){
	easels.push(this);

	this.namespace = namespace;
	this.image = image;
	this.container = $$(image).parent();
	this.canvas = this.container.children('.raphael');
	this.svg = this.canvas.children();
	this.paper = false;
	this.inprocess = false;
	this.scroll = {
		'active':false,
		'top':0,
		'start':{}
	}
}

Easel.prototype = {
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
		this.paper.safari();
	},
	scrolling: function(position){

		if (this.scroll.active) {
			var delta = (this.scroll.start.y - position.y);
			$$('.page-content')[0].scrollTop = this.scroll.top + delta;		
		}
		return false;
	},
	init : function(shapeType){
		var easel = this, mousedown = false;

		easel.paper = new Raphael(this.canvas[0]);

		easel.paper.setViewBox(0,0,this.image.width(),this.image.height(),true);
		easel.paper.setSize('100%', '100%');
		
		easel.display();
		// Correct position of the SVG canvas as the position is absolute
		$$('.page-content').on('scroll',function(){
			easel.display();
		});
		// Correct the size of the SVG canvas
		$$(window).on('resize',function(){
			easel.display();
		});
		easel.initScrolling();

		var drawing = new Drawing(easel);
		drawing.init(shapeType);
	},
	initScrolling: function(){
		var easel = this;

		easel.container.find('.button-cancel').on('click',function(){
			easel.paper.top.remove();
		});

		easel.canvas[0].addEventListener('touchstart',function(e){
			easel.paper.safari();
			//console.log('started '+easels.indexOf(easel));
			easel.scroll.start = Tactile.getPosition(e);
			//console.log($$(easel.canvas[0]).offset());
			easel.scroll.top = $$('.page-content')[0].scrollTop;
			easel.scroll.active = true;
		}, false);
		easel.canvas[0].addEventListener('touchmove',function(e){
			easel.paper.safari();
			if (!easel.inprocess) {
				//console.log('moving '+easels.indexOf(easel));
				easel.scrolling(Tactile.getPosition(e));
			}
		}, false);
		easel.canvas[0].addEventListener('touchend',function(e){
			easel.paper.safari();
			easels.forEach(function(entry){
				//console.log('cancelled');
				entry.scroll.active = false;
				entry.display();
			});
		}, false);
	}
}
