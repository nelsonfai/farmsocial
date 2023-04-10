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

function deleteConfirm(event){
    
    if (confirm('Are you sure you want to Delete this item')) {
} else {
    event.preventDefault();
}
}


