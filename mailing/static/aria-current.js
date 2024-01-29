document.getElementsByClassName("list-group")[0].addEventListener("mouseover",function(e) {
    if (e.target && e.target.matches("a.list-group-item")) {
        e.target.classList.add("active");
        e.target.setAttribute("aria-current", "page");
    }
});

document.getElementsByClassName("list-group")[0].addEventListener("mouseout",function(e) {
    if (e.target && e.target.matches("a.list-group-item")) {
        e.target.classList.remove("active");
        e.target.removeAttribute("aria-current");
    }
});