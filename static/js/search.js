let input = document.getElementById("searchBar");
let ul = document.getElementById("listToSearch");
let pos = ul.offsetTop

function searchBar() {
    let filter = input.value.toUpperCase();
    let li = ul.getElementsByTagName("li");
    for (let i = 0; i < li.length; i++) {
        let a = li[i].getElementsByTagName("a")[0];
        let txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

input.addEventListener("keypress", function(event){
  if (event.key === "Enter") {
    event.preventDefault();
    window.scroll({
      top: pos,
      left: 0,
      behavior: 'smooth'
    });
    // document.getElementById("myBtn").click();
  }
})
