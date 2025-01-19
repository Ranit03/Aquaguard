const scroll = new LocomotiveScroll({
    el: document.querySelector('#main'),
    smooth: true
});
function updateTime() {
    const timeElement = document.getElementById("time");
    const now = new Date();
    const options = {
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        hour12: true,
        timeZone: "Asia/Kolkata"  // Adjust for IST
    };
    timeElement.textContent = now.toLocaleTimeString("en-US", options);
}

// Update time every second
setInterval(updateTime, 1000);
updateTime(); // Call once to set the initial time immediately

function firstPageAnim(){
    var tl = gsap.timeline();

    tl.from("#nav", {
        y:'-10',
        opacity: 0,
        duration: 1.5,
        ease: Expo.easeInOut
    })

    .to(".boundingelem", {
        y:'0',
        duration: 2,
        ease: Expo.easeInOut,
        delay:-1,
        stagger:.2
    })

    .from("#herofooter", {
        y:-10,
        opacity: 0,
        duration: 1.5,
        delay:-.1,
        ease: Expo.easeInOut
    })
}

var timeout;

function circleOval(){
    // Define default scale value
    var xScale = 1;
    var yScale = 1;

    var xPrevious = 0;
    var yPrevious = 0;
    window.addEventListener("mousemove", function(details){
        clearTimeout(timeout);

        var xDiff = details.clientX - xPrevious;
        var yDiff = details.clientY - yPrevious;
        
        xScale = gsap.utils.clamp(.8, 1.2, xDiff);
        yScale = gsap.utils.clamp(.8, 1.2, yDiff);

        xPrevious = details.clientX;
        yPrevious = details.clientY;

        circleMouseFollower(xScale, yScale);
        timeout = setTimeout(function(){
            const adjustedX = details.clientX * 0.8; // 80% of the clientX value
            document.querySelector("#miniCircle").style.transform = `translate(${adjustedX}px, ${details.clientY}px) scale(1, 1)`;
        }, 100);
    });
}

function circleMouseFollower(xScale, yScale){
    window.addEventListener("mousemove", function(details){
        const adjustedX = details.clientX * 0.8; // 80% of the clientX value
        document.querySelector("#miniCircle").style.transform = `translate(${adjustedX}px, ${details.clientY}px) scale(${xScale}, ${yScale})`;
    });
}

circleOval();
circleMouseFollower();
firstPageAnim();

document.querySelectorAll(".elem").forEach(function(elem){
    var rotate = 0;
    var diff_Rot = 0;
    elem.addEventListener("mouseleave", function(dets){
        gsap.to(elem.querySelector("img"), {
            opacity: 0,
            ease: Power3,
            duration: .5
        });
    });
    elem.addEventListener("mousemove", function(dets){
        var diff = dets.clientY - elem.getBoundingClientRect().top;
        diff_Rot = dets.clientX - rotate;
        rotate = dets.clientX;
        
        const adjustedX = dets.clientX * 0.8; // 80% of the clientX value
        
        gsap.to(elem.querySelector("img"), {
            opacity: 1,
            ease: Power3,
            top: diff,
            left: adjustedX, // Adjust the left position
            rotate: gsap.utils.clamp(-20, 20, diff_Rot * .5)
        });
    });
});
