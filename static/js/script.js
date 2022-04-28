updateBtn = document.querySelectorAll(".update-cart")

for(i=0; i<updateBtn.length; i++){
    updateBtn[i].addEventListener('click',function(){
    var foodId = this.dataset.food
     var action = this.dataset.action
     console.log("food:",foodId, "action:", action)
     console.log("user",user)  
     if(user ==="AnonymousUser"){
         console.log("User not Logged in")
		 addCookieItem(foodId, action)
     }else{
        updateUserOrder(foodId, action)
		location.reload()
     }
    })
}

function updateUserOrder(foodId, action){
	console.log('User is authenticated, sending data...')

		var url = '/updateItem/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'foodId':foodId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log(data)
			location.reload()
		});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}