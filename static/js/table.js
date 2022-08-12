// weiter update the order in a table
let updateTable = document.getElementsByClassName('update-table')

for (i = 0; i < updateTable.length; i++) {
	updateTable[i].addEventListener('click', function(){
		let productId = this.dataset.product
		let action = this.dataset.action
		updateUserOrder(productId, action)

	})
}

function updateUserOrder(productId, action){
		let url = `/staff/${restaurant}/${table}/update_table/`
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
                 'X-CSRFToken': csrftoken
			},
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

//weiter closed a order in a table
document.getElementById('make-payment').addEventListener('click', function(e){
		let userFormData ={
		  'name':`${table}`,
		}
    let url = `/staff/${restaurant}/${table}/process_table/`
    fetch(url, {
    	method:'POST',
    	headers:{
    		'Content-Type':'applicaiton/json',
    		'X-CSRFToken':csrftoken,
    	},
    	body:JSON.stringify({'form':userFormData}),

    })
    .then((response) => response.json())
    .then((data) => {
      Swal.fire(
        'Pedido realizado',
        `Pedido ${table} fue enviado a cocina `,
        'success'
      ).then((result) => {
        document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

        location.reload()
      })
      cart = {}
      }
    )
})
