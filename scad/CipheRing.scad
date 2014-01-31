use <Write.scad>

// PARAMETERS:START //
// The pattern as an array of arrays of 1/0 pixels
pattern = [
    [1,1,1,0,1,1,1,0,0,0,1,1,1,0,1,1,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,1,1,0,1,1,1,0,1,0,1,1,1,0,0,0,1]
];

// Initials: 2 x 2 letters
initials1="AB";
initials2="CD";

// Ring radius (in mm)
ringRadius = 8.28;

// PARAMETERS:END //

// Eye distance (in mm, fixed)
eyeDistance = 150;

pixelWidth = ringRadius/9;
pixelHeight = ringRadius/7.1429;
ringWall = 1;

xPixels = len(pattern[0]);
yPixels = len(pattern);
ringResolution=80;
deltaX=atan(pixelWidth/eyeDistance); //how many degrees per pixel angle from the viewing point.
deltaY=atan(pixelHeight/eyeDistance); //how many degrees per pixel angle from the viewing point.

rotate([180,0,0]) difference() {
        difference() {
//          cylinder(h=pixelHeight*(yPixels+6), r=ringRadius+ringWall, $fn= ringResolution, center =true);
            scale([1,1,2.1]){sphere(r=ringRadius+ringWall, $fn= ringResolution+30 );}

            translate([0,0,-1])
            cylinder(h=pixelHeight*7+2, r=ringRadius, $fn= ringResolution, center =true);
            //punch the inside text:
//          rotate([90,0,0])
//          cylinder(h=ringRadius*2+.4, r=2, $fn= 3, center =true);
            rotate([0,180,0]){
 writecylinder(initials1,[0,0,0],-ringRadius,0,rotate=0, h=3*pixelHeight, t=.4);
 writecylinder(initials2,[0,0,0],-ringRadius,0,rotate=0, h=3*pixelHeight, t=.4, east=180);
}

        //slice the top and bottom along the radial angle of the sweetspot
            translate([eyeDistance,-ringRadius,0])
            rotate([0,((yPixels+1)/2)*deltaY,180])
            translate([-eyeDistance/2,-ringRadius*2.5,-ringRadius*2])
            cube(size=[eyeDistance*3,ringRadius*3,ringRadius*2],center=false);

            translate([eyeDistance,ringRadius,0])
            rotate([0,((yPixels+1)/2)*deltaY,0])
            translate([-eyeDistance*2,-ringRadius*2.5,0])
            cube(size=[eyeDistance*2,ringRadius*3,ringRadius*2],center=false);
    }

    translate([eyeDistance,0,0]) {
        for(i=[0:xPixels-1]){
            for(j=[0:yPixels-1]){
                rotate([0,(j-(yPixels-1)/2)*deltaY,(i-xPixels*.5+.5)*deltaX])
                translate([-eyeDistance/2,0,0])
                if (pattern[j][i]==1)
                {
                    translate([-eyeDistance/2,0,0])
                    cube(size=[ringRadius*3,pixelWidth*1.08,pixelHeight/2],center=true);
                    echo("textpixel");
                }else if ((j==0 && (i == 7  || i == 13  ))||(j==4 && (i == 3 || i == 9  ))){
                    echo("support pixel");
                }else{
                    translate([-round(rands(0,1,1)[0])*ringRadius*2+ringRadius-eyeDistance/2,0,0])
                    cube(size=[ringRadius*2,pixelWidth*1.08,pixelHeight/2],center=true);
                    echo ("random Pixel");
                }

            }
        }
    }
}
