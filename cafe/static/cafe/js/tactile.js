var Tactile = {
	getMousePosition: function(e,container){
		return {
			'x':e.offsetX,
			'y':e.offsetY
		}
	},
	getTouchPosition: function(e,container){
		e.preventDefault();
		var offset = container.offset();
		return {
			'x' : e.touches[0].pageX - offset.left,
			'y' : e.touches[0].pageY - offset.top
		}
	}	
}