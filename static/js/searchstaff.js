let input = document.getElementById("searchBar");
let div = document.getElementById("listToSearch");
let pos = div.offsetTop
let list = div.getElementsByTagName("select");


function searchBarr() {
    let filter = input.value.toUpperCase();

    for (let i = 0; i < list.length; i++) {
      let options = list[i].getElementsByTagName("option")
      for (let i = 0; i < options.length; i++) {
        let option = options[i]
        let txtValue = option.textContent || option.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            option.style.display = "";

        } else {
            option.style.display = "none";

        }
      }
    }
}

let check = []

for (let i = 0; i < list.length; i++) {
  let options = list[i].getElementsByTagName("option")
  for (let i = 0; i < options.length; i++) {
    let option = options[i]
    if (option.selected){
      check.push(option)
    }
    option.addEventListener("click", function(e){
    let addCheck = true
    for (let i = 0; i < check.length; i++){
        let changeOption = check[i]
        if (option == changeOption){

          changeOption.selected = false
          let newCheck = check.filter(data => data != changeOption)

          check = newCheck
          addCheck = false
          for (let i = 0; i < check.length; i++){
            let newValue = check[i]
            newValue.selected = true
          }
        }else{
          changeOption.selected = true
        }
      }
      if (addCheck){
        check.push(option);
      }

    })
}}


div.addEventListener("click", function(event){
  console.log("new")
})
