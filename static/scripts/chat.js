/*
let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()
let threadId = $('#thread-id').val()
let receiver = $('.send-to-user')


let loc = window.location
let wsStart = 'ws://'

if(loc.protocol === 'https') {
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname
console.log(endpoint)
console.log(loc.pathname)

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e)
    send_message_form.on('submit', function (e){
        e.preventDefault()
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        
       
        let thread_id = threadId
        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': get_active_other_user_id(),
            'thread_id': thread_id
        }
        console.log({'data':data})
        console.log('receiver we care here')

        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log('receiver we care here')
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    let send_to_id = data['send_to']
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}
function newMessage(message, sent_by_id, thread_id) {
	if ($.trim(message) === '') {
		return false;
	}
	let message_element;
	let chat_id = 'chat_' + thread_id
	if(sent_by_id == USER_ID){
	    message_element = `		
        <div class="replied">
            <div class="msg_cotainer_send">
            <p> ${message} </p>  
                <div class="msg_time_send msg_time">now</div>
            </div>
        </div>

	    `
    }
	else{
	    message_element = `   
        <div>                                   
           <div class="msg_cotainer">
                <p>${message} </p> 
                <div class="msg_time">now</div>
            </div>
        </div>
        `

    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
	message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
	input_message.val(null);
}


$('.contact-li').on('click', function (){
    $('.contacts .actiive').removeClass('active')
    $(this).addClass('active')

    // message wrappers
    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id +'"]').addClass('is_active')

})

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}


function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}


*/





$('#send-message-form').submit(function(e){
e.preventDefault();

var msg = $('#input-message').val();
var id= $('#thread-id').val();

$.ajax({
  url: '/chat/sendmessage/',
  dataType: 'json',
  method:'POST',
  data : {
    'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
  'message' : msg,
  'id':id,
},
  success:function(data) {
   let questiondiv = ` <div class="replied">
   <div class="msg_cotainer_send">
   <p> ${msg} </p>  
       <div class="msg_time_send msg_time">now</div>
   </div>
</div>

`
let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
message_body.append($(questiondiv))
input_message.val(null);
  }
});
})


