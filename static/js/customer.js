let url = "/account/customer/update"

let updatedInfo ={
  'name':null,
  'email':null,
  'phone': null,
  'username': null,
}

function updateFormInfo(){
  updatedInfo.name = form.name.value
  updatedInfo.phone = form.phone.value
  updatedInfo.email = form.email.value
  updatedInfo.username = form.username.value
}


let form = document.getElementById('customer-form')
/*submit funcionality*/
form.addEventListener('submit', function(e){
  e.preventDefault()
  updateFormInfo()
  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'applicaiton/json',
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'form':updatedInfo}),

  })
  .then((response) => response.json())
  .then((data) => {
    console.log(data)
    if (data == "success"){
      Swal.fire({
          icon: 'success',
          title: 'Perfil actualizado',
          text: `Su login es: ${form.name.value}, e-mail para acompañar pedidos ${form.email.value} y el telefono para contacto ${form.phone.value}`,
          footer: `<a href="/pedidos/${form.email.value}/">Llevame a mis pedidos</a>`,
      })
    }else if (data == "name"){
      Swal.fire({
          icon: 'error',
          title: 'Nombre ya esta en uso',
          text: `El nombre ${form.name.value} ya esta en uso. Elija otro`,
      })
    }else if (data == 'login'){
      Swal.fire({
          icon: 'error',
          title: 'login ya esta en uso',
          text: `El login ${form.username.value} ya esta en uso. Elija otro`,
      })
    }else{
      Swal.fire({
          icon: 'error',
          title: 'Email ya esta en uso',
          text: `El email ${form.email.value} ya esta en uso. Elija otro`,
      })
    }

  })
})
