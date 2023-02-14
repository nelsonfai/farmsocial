let navlinks = document.getElementById('navlinks');
var ham = document.getElementById('ham');
ham.onclick=function(){
document.body.classList.toggle('ham')
if(document.body.classList.contains('ham')) {

navlinks.style.display='block'
} 
else{

navlinks.style.display='none'
}
}


function topFunction() {
    console.log('message top')
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }

  let cookieModal = document.querySelector(".cookie-consent-modal")
  let cancelCookieBtn = document.querySelector(".btn.cancel")
  let acceptCookieBtn = document.querySelector(".btn.accept")
  
  cancelCookieBtn.addEventListener("click", function (){
      cookieModal.classList.remove("active")
  })
  acceptCookieBtn.addEventListener("click", function (){
      cookieModal.classList.remove("active")
      localStorage.setItem("cookieAccepted", "yes")
  })
  
  setTimeout(function (){
      let cookieAccepted = localStorage.getItem("cookieAccepted")
      if (cookieAccepted != "yes"){
          cookieModal.classList.add("active")
      }
  }, 2000)

function deleteConfirm(event){
    
    if (confirm('Are you sure you want to Delete this item')) {
} else {
    event.preventDefault();
}
}