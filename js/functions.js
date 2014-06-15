function setActiveLink (what) {
    console.log(what);
    if(what != "")
        document.getElementById(what).setAttribute("class", "active");
}

