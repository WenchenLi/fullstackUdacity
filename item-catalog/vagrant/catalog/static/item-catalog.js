// function signInCallback(authResult) {
//   if (authResult.code) {
//     // Hide the sign-in button now that the user is authorized
//     $('#signinButton').attr('style', 'display: none');
//
//     // Send the one-time-use code to the server, if the server responds,
//     // write a 'login successful' message to the web page and then
//     //redirect back to the main restaurants page
//     $.ajax({
//       type: 'POST',
//       url: '/gconnect?state={{STATE}}',
//       processData: false,
//       data: authResult.code,
//       contentType: 'application/octet-stream; charset=utf-8',
//       success: function(result) {
//         // Handle or verify the server response if necessary.
//         if (result) {
//           $('#result').html('Login Successful!</br>' + result + '</br>Redirecting...')
//           setTimeout(function() {
//             window.location.href = "/catalog";
//           }, 4000);
//         } else if (authResult.error) {
//
//           console.log('There was an error: ' + authResult.error);
//         } else {
//           $('#result').html('Failed to make a server-side call. Check your configuration and console.');
//         }
//       }
//     });
//   }
// }
//
// window.fbAsyncInit = function() {
//   FB.init({
//     appId: '805081092958808',
//     xfbml: true,
//     cookie: true,
//     version: 'v2.6'
//   });
// };
//
// (function(d, s, id) {
//   var js, fjs = d.getElementsByTagName(s)[0];
//   if (d.getElementById(id)) {
//     return;
//   }
//   js = d.createElement(s);
//   js.id = id;
//   js.src = "//connect.facebook.net/en_US/sdk.js";
//   fjs.parentNode.insertBefore(js, fjs);
// }(document, 'script', 'facebook-jssdk'));
// // Here we run a very simple test of the Graph API after login is
// // successful.  See statusChangeCallback() for when this call is made.
// function sendTokenToServer() {
//   FB.login(function(response) {
//     if (response.authResponse) {
//       var access_token = FB.getAuthResponse()['accessToken'];
//       console.log('Access Token = ' + access_token);
//       FB.api('/me', function(response) {
//         console.log('Good to see you, ' + response.name + '.');
//
//         $.ajax({
//           type: 'POST',
//           url: '/fbconnect?state={{STATE}}',
//           processData: false,
//           data: access_token,
//           contentType: 'application/octet-stream; charset=utf-8',
//           success: function(result) {
//             // Handle or verify the server response if necessary.
//             if (result) {
//               $('#result').html('Login Successful!</br>' + result + '</br>Redirecting...')
//               setTimeout(function() {
//                 window.location.href = "/catalog";
//               }, 4000);
//
//
//             } else {
//               $('#result').html('Failed to make a server-side call. Check your configuration and console.');
//             }
//           }
//         });
//
//       });
//     } else {
//       console.log('User cancelled login or did not fully authorize.');
//     }
//   }, {
//     scope: ''
//   });
// }
