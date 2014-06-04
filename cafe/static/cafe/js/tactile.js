var Tactile = {
	getMousePosition: function(e,offset){
		return {
			'x':e.offsetX,
			'y':e.offsetY
		}
	},
	getTouchPosition: function(e, offset){
		e.preventDefault();
		var position = {
			'x' : e.touches[0].pageX,
			'y' : e.touches[0].pageY
		}

		if (offset){
			position.x -= offset.left;
			position.y -= offset.top;
		}
		return position;
	}	
}