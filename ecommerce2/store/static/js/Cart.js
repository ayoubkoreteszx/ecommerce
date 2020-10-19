var updateBtns=document.getElementsByClassName('update-cart')
for(let i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productId=this.dataset.product
        var action=this.dataset.action
        var size=this.dataset.size
        console.log("hhhh "+size)

        console.log('product id :',productId,'Action :',action," size",size)

        if(user=='AnonymousUser'){
            addCookieItem(productId,action,size)
        }
        else{
            updateUserOrder(productId,action,size)
        }
    })
}
function addCookieItem(productId,action,size){
     console.log("Not logged in ...")
     newCart=[];
     newCart = Object.keys(cart).map((v)=>{
        return cart[v].size;
      });
      console.log("the array of sizes"+newCart);
     if (action=="add"){
           if(cart[productId]==undefined ){
               cart[productId]={'quantity':1}
               cart[productId]['size']=size
           }
           else{
             for(var i=0;i<newCart.length;i++){
                     if (cart[productId]["size"].indexOf(newCart[i]) !== -1){
                         cart[productId]['quantity']+=1/newCart.length
                         cart[productId]['size']=size
                     }
                     else{ 
                        console.log('the products '+cart[productId]["size"])
                        cart[productId]={'quantity':1}
                        cart[productId]['size']=size
                     }
                }
            } 
}
     if (action=='remove'){
         cart[productId]['quantity']-=1
         if(cart[productId]['quantity']<=0){
               cart[productId]=undefined
               window.open("http://127.0.0.1:8000/product/"+productId);
          }
    }

     console.log("cart",cart)
     document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"
     location.reload()
}
function updateUserOrder(productId,action,size){
    console.log("User is authenticated,sending data...")
    console.log("size test test test test test "+size)
    console.log("TATTATATTTTTTTTTTT",{'productId':productId,'action':action,'size':size})
    var url='/update_item/'
    fetch(url,{ 
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'Accept': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action,'size':size})
    })
    .then(response=>{console.log(response)
        return response.json()})
    .then(data=>{console.log('data',data)
    /*location.reload()*/
     })
    .catch((ex)=>console.log("there is some error",ex))
}