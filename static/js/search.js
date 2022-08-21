let input = document.getElementById("searchBar");
let ul = document.getElementById("listToSearch");
let pos = ul.offsetTop

function searchBar() {
    let filter = input.value.toUpperCase();
    let li = ul.getElementsByTagName("li");
    for (let i = 0; i < li.length; i++) {
        let a = li[i].getElementsByTagName("a")[0];
        let div = li[i].getElementsByTagName("div")[0];
        let p = li[i].getElementsByTagName("p")[0];
        let h4 = li[i].getElementsByTagName("h4")[0];
        let txtValue = a.textContent || a.innerText || div.textContent || div.innerText || p.textContent || p.innerText || h4.textContent || h4.innerText;
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
    console.log(categories)
    if (input.title === "category" && categories.includes(input.value.toLowerCase())){

        window.location.href = `/restaurant/${restaurant}/category/${input.value}`;
    }
    window.scroll({
      top: pos,
      left: 0,
      behavior: 'smooth'
    });
    // document.getElementById("myBtn").click();
  }
})
