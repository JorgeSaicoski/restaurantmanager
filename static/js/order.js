// weiter update the order in a table
let updateOrderBtn = document.getElementsByClassName('update-order')

for (i = 0; i < updateOrderBtn.length; i++) {
	updateOrderBtn[i].addEventListener('click', function(){
		let productId = this.dataset.product
		let action = this.dataset.action
		updateUserOrder(productId, action)

	})
}

function updateUserOrder(productId, action){
		let url = `/staff/${restaurant}/${order}/update_order/`
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
