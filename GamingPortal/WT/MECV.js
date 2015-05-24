"use strict";

var POINT_RADIUS = 4;
var CIRCLE_COLOR = "#9CC1E6";
var POINT_COLOR = "#FFFFFF";


var canvasElem = document.getElementById("canvas");
var canvasPoints = [];
var canvasCircle = null;
var suppressContextMenu = false;
var dragPointIndex = -1;
var img3=document.createElement('img');
img3.src='smoke.png';
var img2=document.createElement('img');
img2.src='drop.png';
var img1=document.createElement('img');
img1.src='water.png';
var img=document.createElement('img');
img.src='fire.png';

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