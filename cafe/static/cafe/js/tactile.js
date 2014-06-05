var Tactile = {
	getPosition : function(e, offset){
		if (e.offsetY)
			return Tactile.getMousePosition(e,offset);
		else
			return Tactile.getTouchPosition(e,offset);
	},
	getMousePosition: function(e, offset){
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