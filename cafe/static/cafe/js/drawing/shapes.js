var shapeTypes = ['ellipse','rectangle','polygon'];

function Shape(drawing,shapeType){
	this.drawing = drawing;
	this.drawing.shapes.push(this);
	this.i = this.drawing.shapes.indexOf(this);
	this.type = shapeType;
	this.element = false;
	this.isInProcess = false;
}
Shape.prototype = {
	create: function(attributes){
		var color = getRandomColor();

		switch (this.type) {
			case 'ellipse':
			this.context.circle(attributes.x, attributes.y, 100);
			break;
			case 'rectangle':
			this.element = new fabric.Rect({
				left: attributes.x,
				top: attributes.y,
				opacity:0.5,
				fill: 'orange',
				stroke:'blue',
				width: 200,
				height: 200
			});
			break;

			case 'polygon':
			this.element = new fabric.Polygon(
				[{x:attributes.x, y:attributes.y},{x:attributes.x+2, y:attributes.y}+2],
				{
					opacity:0.5,
					fill: 'orange',
					stroke:'blue',
					strokeWidth: 5,
					left: attributes.x,
					top: attributes.y
				});
			this.isInProcess = true;
			break;

			default:
			console.log('shape create error - incorrect type');
			break;
		}
		if (this.element){
			this.drawing.easel.fabric.add(this.element);

			if (this.type == 'rectangle'){
				this.drawing.easel.actions.finish();
			}
		}
	},
	update: function(attributes){
		switch (this.type) {
			case 'ellipse':
			this.element.attr({'rx':attributes.rx,'ry':attributes.ry});
			break;
			case 'rectangle':
			this.element.width = attributes.x;
			this.element.height = attributes.y;
			this.drawing.easel.fabric.renderAll();
			break;
			case 'polygon':
			this.element.points.push({x:attributes.x - this.element.left, y:attributes.y - this.element.top});
			break;
			default:
			console.log('shape create error - incorrect type');
			break;
		}
	},
	remove: function(){
		if (this.element)
			this.element.remove();
		this.drawing.shapes.splice(this.i,1);
		delete this;
	}
}