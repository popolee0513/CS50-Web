//fix the problem of Django returns 403 error on POST request with Fetch
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
  const submit = document.querySelector('#submit');
  const newTask = document.querySelector('#Textarea1');
  newTask.onkeyup = () => {
        if (newTask.value.length > 0) {
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }  
  document.querySelectorAll('#close_window').forEach(button =>{
  button.onclick=function(){
  document.querySelector('#Textarea1').value="";  
  }
  });
    
  document.querySelector('#submit').onclick=function(){
  fetch('/create', {
  method: 'POST',
  headers: {
          "X-CSRFToken": getCookie("csrftoken")
          
        },
  body: JSON.stringify({body: document.querySelector('#Textarea1').value})
  })
  document.querySelector('#Textarea1').value="";  
  console.log(document.querySelector('#Textarea1').value);
  //var elem = document.getElementById('index');
  // Simulate clicking on the specified element.
  //elem.click();    
  window.location.reload();  
  };    

  
});
document.addEventListener('DOMContentLoaded', function() {
    // Select all buttons
    document.querySelectorAll('#like').forEach(button => {
        fetch(`/article/${button.dataset.id}`)
        .then(response => response.json())
        .then(info => {
         // Print email
        console.log(info);
        document.querySelector(`#count-${button.dataset.id}`).innerHTML=info["count"]
        });    
          
        // When a button is clicked, switch to that page
        button.onclick = function() {
        fetch(`/article/${this.dataset.id}`,{
         method: 'PUT',
         headers: {
          "X-CSRFToken": getCookie("csrftoken")
         } 
         })
        .then(response => response.json())
        .then(info => {
         // Print email
        console.log(info);
        document.querySelector(`#count-${this.dataset.id}`).innerHTML=info["count"]
        });             
        }; 

    });
});
document.addEventListener('DOMContentLoaded', function(){
document.querySelectorAll('#edit').forEach(button =>{
    button.onclick = function() {

    var text = document.querySelector(`#article-${this.dataset.edit}`).innerHTML;

    document.querySelector("#Textarea2").value=text;
    
    var newtext="";
    document.querySelector("#Textarea2").addEventListener('change', function (event) {
    newtext += event.target.value;
    });    
  
    var temp_id=  this.dataset.edit;  
    document.querySelector("#change").onclick=function(){
        
        var final="";
        if (newtext===""){
            final=text;
        
        }
        else{
            final=newtext;
        }
        
        
        fetch(`/edit/${temp_id}`,{
         method: 'PUT',
         headers: {
          "X-CSRFToken": getCookie("csrftoken")
         } ,
         body: JSON.stringify({content: final})
         })
        //var elem = document.getElementById('index');
 
        // Simulate clicking on the specified element.
        //elem.click();    
        fetch(`/edit/${temp_id}`,{
         method: 'GET'
         })
        .then(response => response.json())
        .then(info => {
         // Print email
        console.log(info);
        document.querySelector("#Textarea2").innerHTML=info["content"];
        window.location.reload();
        });             

        
    };
};      
        
});       
});
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#control_follow').onclick = function() {
        var text = this.innerHTML;
        var people=this.dataset.people;
        if (text==="follow"){
            this.innerHTML="unfollow";
            var count =parseInt(document.querySelector(`#data-follower-${this.dataset.people}`).innerHTML);
            count+=1;
            document.querySelector(`#data-follower-${this.dataset.people}`).innerHTML=count;
            
        }
        else{
            this.innerHTML="follow";
            var count =parseInt(document.querySelector(`#data-follower-${this.dataset.people}`).innerHTML);
            count-=1;
            document.querySelector(`#data-follower-${this.dataset.people}`).innerHTML=count;
        }
        
        fetch("/follow_control",{
         method: 'POST',
         headers: {
          "X-CSRFToken": getCookie("csrftoken")
         } ,
         body: JSON.stringify({people: people,state:text})
         })
    }
});

/*
document.addEventListener('DOMContentLoaded', function(){
document.querySelectorAll('#panel-following').forEach(button =>{
    button.onclick = function() {
    console.log("check");
    fetch(`/check/${this.dataset.following}?status=following`,{
         method: 'GET'
         })
    .then(response => response.json())
    .then(info => {
         // Print email
        console.log(info);
        var post = document.createElement('ul');
        console.log(info["content"]);
        for (var step = 0; step <info["content"].length ; step++){
        const data = document.createElement('li');    
        data.innerHTML=info["content"][step];
        post.append(data);
         
    }
        console.log(post);   
        document.querySelector(`#modal-following-body-${this.dataset.following}`).append(post);
        
        });                   
    } 
});
    
});
document.addEventListener('DOMContentLoaded', function(){
document.querySelectorAll('#panel-follower').forEach(button =>{
    button.onclick = function() {
    console.log("check");
    fetch(`/check/${this.dataset.follower}?status=follower`,{
         method: 'GET'
         })
    .then(response => response.json())
    .then(info => {
         // Print email
        console.log(info);
        var post = document.createElement('ul');
        console.log(info["content"]);
        for (var step = 0; step <info["content"].length ; step++){
        const data = document.createElement('li');    
        data.innerHTML=info["content"][step];
        post.append(data);
         
    }
        console.log(post);   
        document.querySelector(`#modal-follower-body-${this.dataset.follower}`).append(post);
        
        });                   
    } 
});
    
});
*/

