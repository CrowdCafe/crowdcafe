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
	this.control = {}
	if ($$(image).attr('min-shapes'))
		this.control.min_shapes = parseInt($$(image).attr('min-shapes'));
	if ($$(image).attr('max-shapes'))
		this.control.max_shapes = parseInt($$(image).attr('max-shapes'));
	
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
	qualityCheck : function(){
		var response = {'correct':true};

		this.drawing.createInputHidden('[name=taskForm]');
		var shapes_amount = 0;
		if (this.drawing.shapes){
			shapes_amount=this.drawing.shapes.length;
		}
		if (this.control.min_shapes && shapes_amount < this.control.min_shapes){
			response.correct = false;
			response.description = 'the min amount of shapes should be '+this.control.min_shapes;
		}
		if (this.control.max_shapes && shapes_amount > this.control.max_shapes){
			response.correct = false;
			response.description = 'the max amount of shapes should be '+this.control.max_shapes;
		}
		
		return response;
		
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
			var thelastshape = easel.drawing.getLastShape();
			if (thelastshape){
				thelastshape.remove();
			}
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
