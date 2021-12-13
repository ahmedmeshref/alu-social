function changeActive(e) {
    console.log(e.target)
    var elems = document.querySelector(".active");
    if (elems !== null) {
        elems.classList.remove("active");
    }
    e.target.className = "active";
}