var easels = [];

function Easel(canvas, size, namespace, imageInstance) {
	easels.push(this);
	this.size = size;
	this.namespace = namespace;
	this.imageInstance = imageInstance;
	this.canvas = $$(canvas);
	this.container = this.canvas.parent();
	this.canvas[0].width = this.container.width();
	this.canvas[0].height = this.size.height * this.canvas[0].width / this.size.width;
	this.buttons = {
		start: this.container.find('.shape-start'),
		finish: this.container.find('.shape-finish'),
		remove: this.container.find('.shape-remove')
	}
	var easel = this;
	this.actions = {
		start: function() {
			var easel = this;

		},
		finish: function() {
			easel.drawing.activeShape = false;
			easel.imageBackground.opacity = 1.0;

			var thelastshape = easel.drawing.getLastShape();
			if (thelastshape) {
				thelastshape.element.hasControls = true;
				if (thelastshape.element) {
					thelastshape.element.set({
						fill: 'green',
						borderColor: 'red',
						cornerColor: 'green',
						cornerSize: 20
					});
				}
			}
			easel.fabric.renderAll();
		},
		removeLast: function() {
			easel.buttons.finish.click();
			easel.drawing.activeShape = false;
			var thelastshape = easel.drawing.getLastShape();
			if (thelastshape) {
				thelastshape.remove();
			}
		}
	}

	this.inprocess = false;
	this.control = {};

	if ($$(canvas).attr('min-shapes'))
		this.control.min_shapes = parseInt($$(canvas).attr('min-shapes'));
	if ($$(canvas).attr('max-shapes'))
		this.control.max_shapes = parseInt($$(canvas).attr('max-shapes'));

	this.scroll = {
		'active': false,
		'top': 0,
		'start': {}
	}
}

function getImgSize(src, callback) {
	var newImg = new Image();
	newImg.onload = function() {
		var size = {
			'width': newImg.width,
			'height': newImg.height
		}
		callback(size, newImg);
	}

	newImg.src = src; // this must be done AFTER setting onload
}
Easel.prototype = {
	serialize: function(form) {
		var canvas_data = JSON.stringify(this.fabric);

		if (this.namespace) {
			name = this.namespace + "_serialization";
			if ($$(['name=' + name]).length == 0) {
				var input_hidden = "<input type='hidden' class='shape_data' name='" + this.namespace + "' value='" + canvas_data + "' />";
				$$(form).append(input_hidden);
			} else {
				$$(['name=' + name]).val(canvas_data);
			}
		}
	},
	qualityCheck: function() {
		var response = {
			'correct': true
		};

		var shapes_amount = 0;
		if (this.drawing.shapes) {
			shapes_amount = this.drawing.shapes.length;
		}
		if (this.control.min_shapes && shapes_amount < this.control.min_shapes) {
			response.correct = false;
			response.description = 'the min amount of shapes should be ' + this.control.min_shapes;
		}
		if (this.control.max_shapes && shapes_amount > this.control.max_shapes) {
			response.correct = false;
			response.description = 'the max amount of shapes should be ' + this.control.max_shapes;
		}
		return response;

	},
	scrolling: function(position) {

		if (this.scroll.active) {
			var delta = (this.scroll.start.y - position.y);
			$$('.page-content')[0].scrollTop = this.scroll.top + delta;
		}
		return false;
	},
	init: function(shapeType) {
		var easel = this,
			mousedown = false;
		easel.fabric = new fabric.Canvas(easel.canvas[0].id);
		easel.imageBackground = new fabric.Image(easel.imageInstance, {
			width: easel.canvas.width(),
			height: easel.canvas.height(),
			selectable: false
		});
		easel.fabric.add(easel.imageBackground);
		easel.initScrolling();
		easel.initActions();


		var drawing = new Drawing(easel);
		drawing.init(shapeType);
	},
	initActions: function() {
		var easel = this;
		easel.buttons.start.on('click', easel.actions.start);
		easel.buttons.finish.on('click', easel.actions.finish);
		easel.buttons.remove.on('click', easel.actions.removeLast);
	},
	initScrolling: function() {
		var easel = this;
		easel.canvas[0].addEventListener('touchstart', function(e) {
			//console.log('started '+easels.indexOf(easel));
			easel.scroll.start = Tactile.getPosition(e);
			//console.log($$(easel.canvas[0]).offset());
			easel.scroll.top = $$('.page-content')[0].scrollTop;
			easel.scroll.active = true;
		}, false);
		easel.canvas[0].addEventListener('touchmove', function(e) {
			if (!easel.inprocess) {
				//console.log('moving '+easels.indexOf(easel));
				easel.scrolling(Tactile.getPosition(e));
			}
		}, false);
		easel.canvas[0].addEventListener('touchend', function(e) {
			easels.forEach(function(entry) {
				//console.log('cancelled');
				entry.scroll.active = false;
			});
		}, false);
	}
}