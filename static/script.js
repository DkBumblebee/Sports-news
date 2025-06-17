//This is for the login and logout
function Hide(element){

    //Getting the object for the element
    let domProperty = document.querySelector(element);
    
    console.log(domProperty.style); // For debugging purposes

    domProperty.style.visibility = "hidden";
    domProperty.style.opacity = 0;
}

function Show(element){

    //Getting the DOM object
    let domProperty = document.querySelector(element);

    //domProperty.style.opacity = opacity;
    domProperty.style["visibility"] = "visible";
    domProperty.style.opacity = 1;
}

document.getElementById("swapRegister").addEventListener("click",function(){
    Hide("#login");
    Show("#register");
});

document.getElementById("swapLogin").addEventListener("click",function(){
    Hide("#register");
    Show("#login");
});


