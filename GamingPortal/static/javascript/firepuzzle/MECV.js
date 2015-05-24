
global_score = 0;
var POINT_RADIUS = 4;
var CIRCLE_COLOR = "#9CC1E6";
var POINT_COLOR = "#FFFFFF";


var canvasElem = document.getElementById("canvas");
var canvasPoints = [];
var canvasCircle = null;
var suppressContextMenu = false;
var dragPointIndex = -1;
var img3=document.getElementById('smoke');
//img3.src= "{% static 'images/fire_images/smoke.png' %}";
var img2=document.getElementById('drop');
//img2.src="{% static 'images/fire_images/drop.png'%}";
var img1=document.getElementById('water');
//img1.src="{% static 'images/fire_images/water.png'%}";
var img=document.getElementById('fire');
//img.src="{% static 'images/fire_images/fire.png'%}";

canvasElem.onmousedown = function(e) {
	var xy = getLocalCoordinates(e);
	var nearest = findNearestPoint(xy[0], xy[1]);
	
	// Left mouse button: Add or move point
	if (e.button == 0) {
		if (nearest.dist <= POINT_RADIUS + 2) {
			dragPointIndex = nearest.index;
		} else {
			
			dragPointIndex = canvasPoints.length;
			canvasPoints.push({x: xy[0], y: xy[1]});
			refreshCanvasCircle();
		}
	}
	else if (e.button == 2) {
		if (nearest.dist <= POINT_RADIUS + 2) {
			canvasPoints.splice(nearest.index, 1);
			refreshCanvasCircle();
		}
		suppressContextMenu = nearest.dist <= POINT_RADIUS + 10;
	}
}


canvasElem.onmousemove = function(e) {
	if (dragPointIndex != -1) {
		var xy = getLocalCoordinates(e);
		canvasPoints[dragPointIndex] = {x: xy[0], y: xy[1]};
		refreshCanvasCircle();
	}
}


canvasElem.onmouseup = function(e) {
	if (e.button == 0) {
		var xy = getLocalCoordinates(e);
		canvasPoints[dragPointIndex] = {x: xy[0], y: xy[1]};
		dragPointIndex = -1;
		refreshCanvasCircle();
	}
}


function getLocalCoordinates(e) {
	var x = e.pageX;
	var y = e.pageY;
	for (var elem = canvasElem; elem != null && elem != document.documentElement; elem = elem.offsetParent) {
		x -= elem.offsetLeft;
		y -= elem.offsetTop;
	}
	return [x, y];
}
canvasElem.oncontextmenu = function() {
	var result = !suppressContextMenu;
	suppressContextMenu = false;
	return result;
}


canvasElem.onselectstart = function() { 
	return false;
}


function doClear() {
	canvasPoints = [];
	refreshCanvasCircle();
}
function hello(ctx,x1,y1) {
    return function() {
	ctx.translate(x1,y1);
			ctx.drawImage(img2,-14,-14,28,28);
			ctx.translate(-x1,-y1);
        
    }
}

function doKill() 
{
	var score = 0;
	canvasCircle = makeCircle(canvasPoints);
	var ctx = canvasElem.getContext("2d");
	ctx.clearRect(0, 0, canvasElem.width, canvasElem.height);
	if (canvasCircle != null) {
		ctx.fillStyle = CIRCLE_COLOR;
		ctx.beginPath();
		ctx.arc(canvasCircle.x, canvasCircle.y, canvasCircle.r + POINT_RADIUS, 0, Math.PI * 2, false);
		ctx.fill();
	}
	
	for (var i = 0; i < canvasPoints.length; i++)
	{
		var x1=canvasCircle.x,y1=canvasCircle.y;
		var x2=canvasPoints[i].x,y2=canvasPoints[i].y;
		score+= Math.sqrt((x1-x2)*(x1-x2)) + ((y1-y2)*(y1-y2)) ;
		var m = (y2-y1)/(x2-x1);
		var tt=(x2-x1)/10;
		if(x1<x2){
		var kk=400;
		while(x1<x2)
		{
			x1+=tt;
			y1+=m*tt;
			if(x1>=x2)
			break;
			kk+=400;
			setTimeout(hello(ctx,x1,y1),kk);
			
		}}
		else
		{
			var kk=400;
			while(x2<x1)
		{
			x1+=tt;
			y1+=m*tt;
			if(x2>=x1)
			break;
			kk+=400;
			setTimeout(hello(ctx,x1,y1),kk);
		}	
		}

		ctx.translate(x2,y2);
		ctx.drawImage(img3,-16,-16,32,32);
		ctx.translate(-x2,-y2);
	}
	ctx.translate(canvasCircle.x, canvasCircle.y);
	ctx.drawImage(img1,-20,-20,40,40);
	ctx.translate(-canvasCircle.x,-canvasCircle.y);
	score/=canvasPoints.length;
	score=parseInt(score);
	global_score = score;
	setTimeout(function() {
    	alert("Score: "+score.toString());
	}, 5500);

	
	
}

function doRandom() {
	var scale = Math.min(canvasElem.width, canvasElem.height);
	canvasPoints = [];
	var len = Math.floor((1 - Math.sqrt(Math.random())) * 20) + 2;  
	for (var i = 0; i < len; i++) {
		var r = randomGaussianPair();
		canvasPoints.push({
			x: r[0] * scale * 0.15 + canvasElem.width  / 2,
			y: r[1] * scale * 0.15 + canvasElem.height / 2});
	}
	refreshCanvasCircle();
}


function refreshCanvasCircle() {
	
	canvasCircle = makeCircle(canvasPoints);
	var ctx = canvasElem.getContext("2d");
	ctx.clearRect(0, 0, canvasElem.width, canvasElem.height);
	
	if (canvasCircle != null) {
		ctx.fillStyle = CIRCLE_COLOR;
		ctx.beginPath();
		ctx.arc(canvasCircle.x, canvasCircle.y, canvasCircle.r + POINT_RADIUS, 0, Math.PI * 2, false);
		ctx.fill();
	}
	
	ctx.translate(canvasCircle.x, canvasCircle.y);
	ctx.drawImage(img1,-20,-20,40,40);
	ctx.translate(-canvasCircle.x,-canvasCircle.y);
	ctx.fillStyle = POINT_COLOR;
	for (var i = 0; i < canvasPoints.length; i++) {
		ctx.translate(canvasPoints[i].x, canvasPoints[i].y);
		ctx.drawImage(img,-12,-12,24,24);
		ctx.translate(-canvasPoints[i].x,-canvasPoints[i].y);
		
		
	}
	
}


function findNearestPoint(x, y) {
	var nearestIndex = -1;
	var nearestDist = Infinity;
	for (var i = 0; i < canvasPoints.length; i++) {
		var d = distance(canvasPoints[i].x, canvasPoints[i].y, x, y);
		if (d < nearestDist) {
			nearestIndex = i;
			nearestDist = d;
		}
	}
	return {dist: nearestDist, index: nearestIndex};
}


function randomGaussianPair() {
	var x, y, magsqr;
	do {
		x = Math.random() * 2 - 1;
		y = Math.random() * 2 - 1;
		magsqr = x * x + y * y;
	} while (magsqr >= 1 || magsqr == 0);
	var temp = Math.sqrt(-2 * Math.log(magsqr) / magsqr);
	return [x * temp, y * temp];
}

function makeCircle(points) {
	
	var shuffled = points.slice(0);
	for (var i = points.length - 1; i >= 0; i--) {
		var j = Math.floor(Math.random() * (i + 1));
		j = Math.max(Math.min(j, i), 0);
		var temp = shuffled[i];
		shuffled[i] = shuffled[j];
		shuffled[j] = temp;
	}
	
	
	var c = null;
	for (var i = 0; i < shuffled.length; i++) {
		var p = shuffled[i];
		if (c == null || !isInCircle(c, p))
			c = makeCircleOnePoint(shuffled.slice(0, i + 1), p);
	}
	return c;
}

function makeCircleOnePoint(points, p) {
	var c = {x: p.x, y: p.y, r: 0};
	for (var i = 0; i < points.length; i++) {
		var q = points[i];
		if (!isInCircle(c, q)) {
			if (c.r == 0)
				c = makeDiameter(p, q);
			else
				c = makeCircleTwoPoints(points.slice(0, i + 1), p, q);
		}
	}
	return c;
}

function makeCircleTwoPoints(points, p, q) {
	var temp = makeDiameter(p, q);
	var containsAll = true;
	for (var i = 0; i < points.length; i++)
		containsAll = containsAll && isInCircle(temp, points[i]);
	if (containsAll)
		return temp;
	
	var left = null;
	var right = null;
	for (var i = 0; i < points.length; i++) {
		var r = points[i];
		var cross = crossProduct(p.x, p.y, q.x, q.y, r.x, r.y);
		var c = makeCircumcircle(p, q, r);
		if (c == null)
			continue;
		else if (cross > 0 && (left == null || crossProduct(p.x, p.y, q.x, q.y, c.x, c.y) > crossProduct(p.x, p.y, q.x, q.y, left.x, left.y)))
			left = c;
		else if (cross < 0 && (right == null || crossProduct(p.x, p.y, q.x, q.y, c.x, c.y) < crossProduct(p.x, p.y, q.x, q.y, right.x, right.y)))
			right = c;
	}
	return right == null || left != null && left.r <= right.r ? left : right;
}


function makeCircumcircle(p0, p1, p2) {
	
	var ax = p0.x, ay = p0.y;
	var bx = p1.x, by = p1.y;
	var cx = p2.x, cy = p2.y;
	var d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2;
	if (d == 0)
		return null;
	var x = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d;
	var y = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d;
	return {x: x, y: y, r: distance(x, y, ax, ay)};
}


function makeDiameter(p0, p1) {
	return {
		x: (p0.x + p1.x) / 2,
		y: (p0.y + p1.y) / 2,
		r: distance(p0.x, p0.y, p1.x, p1.y) / 2
	};
}



var EPSILON = 1e-12;

function isInCircle(c, p) {
	return c != null && distance(p.x, p.y, c.x, c.y) < c.r + EPSILON;
}


function crossProduct(x0, y0, x1, y1, x2, y2) {
	return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0);
}


function distance(x0, y0, x1, y1) {
	return Math.sqrt((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1));
}


$('#submit-button').click(function() {
   $.ajax({
      type:'POST',
				url:'/games/save_score/',
				data:{
					'game_id':5,
					'score':global_score,
				},

      error: function() {
         //$('#info').html('<p>An error has occurred</p>');
      },
   });
});