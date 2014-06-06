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
	createInputHidden : function(form){
		var data = '';
		switch (this.type) {
			case 'ellipse':
			data = this.element.attr('x')+';';
			data += +this.element.attr('y')+';';
			data += +this.element.attr('rx')+';';
			data += +this.element.attr('ry')+';';
			break;
			case 'rectangle':
			data = this.element.attr('x')+';';
			data += +this.element.attr('y')+';';
			data += +this.element.attr('width')+';';
			data += +this.element.attr('height')+';';
			break;
			default:
			console.log('shape create error - incorrect type');
			break;
		}
		var input_hidden = "<input type='hidden' name='"+this.drawing.easel.namespace+"_"+this.i+"_"+this.type+"' value='"+data+"'>";
		$$(form).append(input_hidden);
	}
}