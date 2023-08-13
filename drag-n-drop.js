function dragElement(element) {
    let startX = 0, startY = 0, endX = 0, endY = 0;
    element.onmousedown = dragStart;
    element.ontouchstart = dragStart;

    function dragStart(e) {
        e = e || window.event;
        e.preventDefault();
        // mouse cursor position at start
        if (e.clientX) {  // mousemove
            startX = e.clientX;
            startY = e.clientY;
        } else { // touchmove - assuming a single touchpoint
            startX = e.touches[0].clientX
            startY = e.touches[0].clientY
        }
        document.onmouseup = dragStop;
        document.ontouchend = dragStop;
        document.onmousemove = elementDrag;  // call whenever the cursor moves
        document.ontouchmove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate new cursor position
        if (e.clientX) {
            endX = startX - e.clientX;
            endY = startY - e.clientY;
            startX = e.clientX;
            startY = e.clientY;
        } else {
            endX = startX - e.touches[0].clientX;
            endY = startY - e.touches[0].clientY;
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }
        // set the new position
        const zIndex = CURRENT_Z_INDEX;
        for (const div of getUnited(element)) {
            div.style.left = (div.offsetLeft - endX) + 'px';
            div.style.top = (div.offsetTop - endY) + 'px';
            div.style.zIndex = zIndex;
        }
        CURRENT_Z_INDEX++;
    }

    function dragStop() {
        // stop moving on touch end / mouse btn is released
        document.onmouseup = null;
        document.onmousemove = null;
        document.ontouchend = null;
        document.ontouchmove = null;
        checkIfAssembled(element)
    }
}
