let updateBtns = document.getElementsByClassName('update-order')





for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		let productId = this.dataset.product
    let orderId = this.dataset.order
    let action = this.dataset.action
		updateUserOrder(productId, orderId,action)
	})
}

function updateUserOrder(productId, orderId, action){
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
