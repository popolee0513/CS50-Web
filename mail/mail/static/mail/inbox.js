document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
 load_mailbox('inbox');
});
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
document.addEventListener('DOMContentLoaded', function(){
document.querySelector("#compose-form").onsubmit= function(){
fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value})
})
.then(response => response.json())
//Cannot set property 'innerHTML' of null 
//js代碼從上往下執行時，沒有找到合適的標籤而出錯。類似於在編程中使用一個未定義的變量，所以一定要在使用變量之前對其進行定義。
.then(result => {
    if (result["message"]  === undefined ){
       alert(`${result["error"]}`);
          
    }    
    else{
      
       alert(`${result["message"]}`);
    } 
});
}
});

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = ''
  const element = document.createElement('div'); 
  element.innerHTML = `<h3 id ="check" value='${mailbox}'>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.querySelector('#emails-view').append(element);
  fetch(`/emails/${mailbox}`) 
  .then(response => response.json())
  .then(emails => {
   emails.forEach(add_post);
});
}
function add_post(contents) {
const element = document.createElement('div'); 
      element.setAttribute("data-id",contents["id"]);
const check = document.querySelector('#check').innerText;

if (check==='Sent'){
    var title=contents["recipients"];
}
else{
    var title=contents["sender"];
}


element.innerHTML = `<div class="card" >`
if (contents["read"]===true){

    
element.innerHTML +=  `<div class="card-body"><div class="row"><div class="col-3">${title}</div ><div class="col-3" >${contents["subject"]}</div><div class="col-6 style="text-align:right;">${contents["timestamp"]}</div></div></div></div>`;
}
 
else{
element.innerHTML +=` <div class="card-body bg-light"><div class="row"><div class="col-3">${title}</div ><div class="col-3" >${contents["subject"]}</div><div class="col-6 style="text-align:right;">${contents["timestamp"]}</div></div></div></div>`;
}
element.addEventListener('click', function() {
console.log('This element has been clicked!')
fetch(`/emails/${this.dataset.id}`)
.then(response => response.json())
.then(email => {
    const element = document.createElement('div');
    if (email["archived"]===true){
        element.innerHTML = `<div>From: ${email["sender"]}</div><div>To: ${email["recipients"]}</div><div>Subject: ${email["subject"]}</div><div>TimeStamp: ${email["timestamp"]}</div><br><div><button  id ="click" type="button" class="btn btn-sm btn-outline-primary">unarchive</button></div><hr><div>${email["body"]}</div></div>`;
    }
    else{
    element.innerHTML = `<div>From: ${email["sender"]}</div><div>To: ${email["recipients"]}</div><div>Subject: ${email["subject"]}</div><div>TimeStamp: ${email["timestamp"]}</div><br><div><button  id ="click" type="button" class="btn btn-sm btn-outline-primary">archive</button>&nbsp;<button id="reply" type="button" class="btn btn-sm btn-outline-primary">reply</button></div><hr><div>${email["body"]}</div>`;
    }
   
    document.querySelector('#emails-view').innerHTML = '';
    document.querySelector('#emails-view').append(element);
    
    fetch(`/emails/${this.dataset.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
    })
    var id= email['id'];
    document.querySelector('#click').addEventListener('click',function(){
    console.log('This element has been clicked!');
    fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
    archived: document.querySelector('#click').innerText==='archive'
    })
    })

    if (document.querySelector('#click').innerText==='archive'){
        load_mailbox('archive'); 
    }
    else{
        load_mailbox('inbox'); 
    }    
        
    });
    
    document.querySelector('#reply').addEventListener('click',function(){
    console.log('This element has been clicked!');
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = email["sender"];
    if (email["subject"].includes("Re:")===true){
        var sub = email["subject"];
        }
    else{
        var sub="Re: "+email["subject"];
        
    }
    document.querySelector('#compose-subject').value =sub;
        
    var p=email["body"]
    var newp=p.replaceAll('<br>', '\n');
    document.querySelector('#compose-body').value ="\n\nOn "+email["timestamp"]+" "+email["sender"]+" wrote:\n"+newp;
            
    });
});
});

document.querySelector('#emails-view').append(element);
};
































