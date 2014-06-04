function Drawing(image){

	this.image = image;
	this.container = $$(image).parent();
	this.canvas = this.container.children('.raphael');
	this.svg = this.canvas[0];
	this.paper = false;

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
	
	init : function(){
		var drawing = this;

		drawing.paper = new Raphael(this.svg, this.image.width(), this.image.height()), mousedown = false;
		
		drawing.correctSize();
		drawing.correctPosition();
		
		// Correct position of the SVG canvas as the position is absolute
		$$('.page-content').on('scroll',function(){
			drawing.correctPosition();
		});
		// Correct the size of the SVG canvas
		$$(window).on('resize',function(){
			drawing.correctSize();
		});

		drawing.container.find('.button-cancel').on('click',function(){
			drawing.paper.top.remove();
		});
	}
}
