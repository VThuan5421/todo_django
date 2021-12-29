const date = new Date().toDateString() ;
const setdate = document.querySelector(".setdate");
setdate.innerHTML = date;

setInterval(function(){
    const time = new Date().toLocaleTimeString();
    const settime = document.querySelector(".settime");
    
    settime.innerHTML = time;
},500);


