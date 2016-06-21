
 window.fbAsyncInit = function() {
   FB.init({
     appId      : '805081092958808',
     xfbml      : true,
     cookie : true,
     version    : 'v2.6'
   });
 };

 (function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));
// Here we run a very simple test of the Graph API after login is
// successful.  See statusChangeCallback() for when this call is made.
function sendTokenToServer() {
  FB.getLoginStatus(function(response) {
if (response.status === 'connected') {
  var accessToken = response.authResponse.accessToken;
  console.log(access_token);
  console.log('Welcome!  Fetching your information.... ');
  FB.api('/me', function(response) {
    console.log('Successful login for: ' + response.name);
   $.ajax({
    type: 'POST',
    url: '/fbconnect?state={{STATE}}',
    processData: false,
    data: access_token,
    contentType: 'application/octet-stream; charset=utf-8',
    success: function(result) {
      // Handle or verify the server response if necessary.
      if (result) {
        $('#result').html('Login Successful!</br>'+ result + '</br>Redirecting...')
       setTimeout(function() {
        window.location.href = "/restaurant";
        }, 4000);
       }
      } );
    }
  }}}}}
}
else {
  $('#result').html('Failed to make a server-side call. Check your configuration and console.');
   });
  });
}