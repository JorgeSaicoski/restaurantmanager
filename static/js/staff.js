let updateBtns = document.getElementsByClassName('update-order')

let btnDelivered = document.getElementsByClassName('btn-delivered')

//kitchen secion (if the item was did or no)

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		let productId = this.dataset.product
    let orderId = this.dataset.order
    let action = this.dataset.action
		updateOrder(productId, orderId,action)
	})
}

function updateOrder(productId, orderId, action){
		let url = `/staff/${restaurant}/update_item/`
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
                 'X-CSRFToken': csrftoken
			},
			body:JSON.stringify({'productId':productId, 'orderId':orderId, 'action':action, 'restaurant':restaurant})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

for (i = 0; i < btnDelivered.length; i++) {
	btnDelivered[i].addEventListener('click', function(){
		let productId = this.dataset.product
    let orderId = this.dataset.order
		let mode = this.dataset.mode
		updateOrderItem(productId, orderId, mode)
	})
}

// secion weiter

// if it was delivered (for the delivery or the customer)

function updateOrderItem(productId, orderId, mode){
		let url = `/staff/${restaurant}/delivery_item/`
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
                 'X-CSRFToken': csrftoken
			},
			body:JSON.stringify({'productId':productId, 'orderId':orderId, 'mode':mode, 'restaurant':restaurant})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}
