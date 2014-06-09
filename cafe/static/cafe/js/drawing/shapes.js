var shapeTypes = ['ellipse','rectangle'];

function Shape(drawing,shapeType){
	this.drawing = drawing;
	this.drawing.shapes.push(this);
	this.i = this.drawing.shapes.indexOf(this);
	this.type = shapeType;
	this.element = false;
}
Shape.prototype = {
	create: function(attributes){
		var color = getRandomColor();

		switch (this.type) {
			case 'ellipse':
			this.element = this.drawing.easel.paper.ellipse(attributes.x, attributes.y, attributes.rx,attributes.ry);
			break;
			case 'rectangle':
			this.element = this.drawing.easel.paper.rect(attributes.x, attributes.y, attributes.rx,attributes.ry);
			break;
			default:
			console.log('shape create error - incorrect type');
			break;
		}
		if (this.element)
			this.element.attr({ stroke: color,'stroke-width':5,fill:color,'fill-opacity':0.5 });	
		this.drawing.easel.paper.safari();
	},
	update: function(attributes){
		switch (this.type) {
			case 'ellipse':
			this.element.attr({'rx':attributes.rx,'ry':attributes.ry});
			break;
			case 'rectangle':
			this.element.attr({'width':attributes.rx,'height':attributes.ry});
			break;
			default:
			console.log('shape create error - incorrect type');
			break;
		}
		this.drawing.easel.paper.safari();
	},
	remove: function(){
		if (this.element)
			this.element.remove();
		this.drawing.shapes.splice(this.i,1);
		delete this;
	},
	createInputHidden : function(form){
		var data = '';
		console.log(this);
		switch (this.type) {
			
			case 'ellipse':
			data = (this.element.attr('x')/this.drawing.easel.canvas.width()).toFixed(4)+';';
			data += (this.element.attr('y')/this.drawing.easel.canvas.height()).toFixed(4)+';';
			data += (this.element.attr('rx')/this.drawing.easel.canvas.width()).toFixed(4)+';';
			data += (this.element.attr('ry')/this.drawing.easel.canvas.height()).toFixed(4)+';';
			break;

			case 'rectangle':
			data = (this.element.attr('x')/this.drawing.easel.canvas.width()).toFixed(4)+';';
			data += (this.element.attr('y')/this.drawing.easel.canvas.height()).toFixed(4)+';';
			data += (this.element.attr('width')/this.drawing.easel.canvas.width()).toFixed(4)+';';
			data += (this.element.attr('height')/this.drawing.easel.canvas.height()).toFixed(4)+';';
			break;
			
			default:
			console.log('shape create error - incorrect type');
			break;
		}

		var input_hidden = "<input type='hidden' class='shape_data' name='"+this.drawing.easel.namespace+"_"+this.i+"_"+this.type+"' value='"+data+"' />";
		console.log(input_hidden);
		console.log($$(form));
		$$(form).append(input_hidden);
	}
}