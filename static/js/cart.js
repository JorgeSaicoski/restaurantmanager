let updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		let productId = this.dataset.product
		let action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)
    console.log(restaurant)
		if (user == 'AnonymousUser'){
			console.log('User is not authenticated')


		}else{
			updateUserOrder(productId, action)
		}

	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		let url = `/restaurant/${restaurant}/update_item/`
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
        'X-CSRFToken': csrftoken
			},
			body:JSON.stringify({'productId':productId, 'action':action, 'restaurant':restaurant})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}
