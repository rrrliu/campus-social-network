// function like() {
//   $(".like").css("display", "none");
//   $(".unlike").css("display", "block");
// }
//
// function unlike() {
//   $(".like").css("display", "block");
//   $(".unlike").css("display", "none");
// }

function filterSelection(c) {
  var x, i;
  x = document.getElementsByClassName("filterDiv");
  if (c == "all") c = "";
  for (i = 0; i < x.length; i++) {
    w3RemoveClass(x[i], "show");
    if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
  }
}

function w3AddClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {element.className += " " + arr2[i];}
  }
}

function w3RemoveClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}

// Add active class to the current button (highlight it)
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function(){
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}




function onSignIn(googleUser) {
  let profile = googleUser.getBasicProfile();
  $("body, html").css("overflow", "visible");
  $(".g-signin2").css("display", "none");
  $(".circle").css("display", "none");
  $(".confirm").css("display", "block");
  $("#pic").attr('src', profile.getImageUrl());
  $("#email").text(profile.getEmail());
  $("#name").text(profile.getName());
  $("#pic_input").attr("value", profile.getImageUrl());
  $("#email_input").attr("value", profile.getEmail());
  $("#firstname_input").attr("value", profile.getGivenName());
  $("#lastname_input").attr("value", profile.getFamilyName());

  let id_token = googleUser.getAuthResponse().id_token;
}

function signOut() {
let auth2 = gapi.auth2.getAuthInstance();
auth2.signOut().then(function() {
  $(".circle").css("display", "block");
  $(".g-signin2").css("display", "block");
  $(".confirm").css("display", "none");
  $("body, html").css("overflow", "hidden");
  })

}
