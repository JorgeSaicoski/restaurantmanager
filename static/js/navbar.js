let containers = document.getElementsByClassName('navbar-container')
let navbar = document.getElementById('navbar')
let closer = document.getElementById("close-navbar")

function deactivedContainers(){
  //get all containers
  for (let i = 0; i < containers.length; i++) {
    //deactived navbar
    navbar.classList.remove("navbar-active")
    navbar.classList.add("navbar")
    closer.classList.remove("close-active")
    //get specifc container
    let container = containers[i]
    container.classList.add("wait")
    //close it
    container.classList.remove("navbar-container-active")
    closer.classList.add("wait")

  }
}

function activedContainer(container){
  deactivedContainers()
  //active navbar
  navbar.classList.add("navbar-active")
  navbar.classList.remove("navbar")
  closer.classList.add("close-active")

  //active container
  container.classList.add("navbar-container-active")
}

//get all containers
for (let i = 0; i < containers.length; i++) {
  //get specifc container and blocker
  let container = containers[i]
  let block = container.getElementsByClassName('navbar-block')
  //if it is clicked it is opened
  container.addEventListener("click", function(e){
    activedContainer(container)
  })
}

//deactived when click outside the navbar
closer.addEventListener("click", function(e){
  deactivedContainers()
})
