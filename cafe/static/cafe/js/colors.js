var ios7colors = ['#FF2A68','#FF5E3A','#FFCD02','#0BD318','#5AC8FB','#1D62F0','#5856D6','#C643FC','#2B2B2B','#898C90','#FF3B30','#FF9500'];

function getRandomNumberFromRange(min, max) {
    return Math.round(Math.random() * (max - min) + min);
}

function getRandomColor(){
	var index = getRandomNumberFromRange(0,ios7colors.length-1);
	return ios7colors[index];
}