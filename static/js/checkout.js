if (delivery == 'False'){
  document.getElementById('delivery-info').innerHTML = ''
}
/*if it have a account it not need a customer info*/
if (user != 'AnonymousUser'){
  document.getElementById('user-info').innerHTML = ''
}
/*if it is not delivery and it is logged it dont need a form*/
if (delivery == 'False' && user != 'AnonymousUser'){
  //Hide entire form if user is logged in and delivery is false
  document.getElementById('form-wrapper').classList.add("hidden");
  //Show payment if logged in user wants to buy an item that does not require delivery
  document.getElementById('payment-info').classList.remove("hidden");
}
/*form*/
let form = document.getElementById('form')
/*submit funcionality*/
form.addEventListener('submit', function(e){
  e.preventDefault()
  document.getElementById('form-button').classList.add("hidden");
  document.getElementById('payment-info').classList.remove("hidden");
})
let userFormData ={
  'name':null,
  'email':null,
  'phone': null,
  'total': total,
}
let deliveryInfo = {
  'address':null,
  'city': null,
  'state': null,
  'zipcode':null,
  'restaurant':restaurant,
}
function submitFormData(){

  if (delivery != 'False'){
      deliveryInfo.address = form.address.value
      deliveryInfo.city = form.city.value
      deliveryInfo.state = form.state.value
      deliveryInfo.zipcode = form.zipcode.value
  }
  if (user == 'AnonymousUser'){
      userFormData.name = form.name.value
      userFormData.phone = form.phone.value
      userFormData.email = form.email.value
  }
}
document.getElementById('make-payment').addEventListener('click', function(e){
    submitFormData()
    let url = `/restaurant/${restaurant}/process_order/`
    try{
      fetch(url, {
      	method:'POST',
      	headers:{
      		'Content-Type':'applicaiton/json',
      		'X-CSRFToken':csrftoken,
      	},
      	body:JSON.stringify({'form':userFormData, 'shipping':deliveryInfo}),

      })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data);
        alert('Transaction completed');
        window.location.href = `/restaurant/${restaurant}`
        cart = {}
        document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

        window.location.href = `/restaurant/${restaurant}`
        }
      ).catch(e=>alert("Hay una cuenta con este email. Por favor, realizar login"))
  }catch(e){
    alert(e)
  }
})
