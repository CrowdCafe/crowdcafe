var Tactile = {
	
	latesttap : new Date().getTime(),

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
		if (e.touches && e.touches.length>0){
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
		return false
	},
	checkDouble: function(){
		var now = new Date().getTime();
		var timesince = now - Tactile.latesttap;
		Tactile.latesttap = now;
		if((timesince < 400) && (timesince > 0))
			return true;
		else
			return false;
	}
}