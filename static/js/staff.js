let updateBtns = document.getElementsByClassName('update-order')

let btnDelivered = document.getElementsByClassName('btn-delivered')



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
		updateOrderItem(productId, orderId)
	})
}

function updateOrderItem(productId, orderId){
		console.log(productId,orderId)
		let url = `/staff/${restaurant}/delivery_item/`
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
                 'X-CSRFToken': csrftoken
			},
			body:JSON.stringify({'productId':productId, 'orderId':orderId, 'restaurant':restaurant})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}
