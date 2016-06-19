#multi user blog framework
this is a simple blog framework with basic features:
* security: sha256 with salt to store user information, hmac with secret to set secure user cookie values
* jinja2 template used to make structured html
* regular expression to check valid sign-up information
* User, Post and Post Comment inherent from google.appengine.ext.db
* cookies default expires in 2 weeks

##Functionality
* support multiple users
* users can like others' posts excluding himself/herself
* users can comment on all the posts
* users can edit/delete their own posts and comments



##Run
There is an online version hosts at [here](http://multi-user-blog-wenchen.appspot.com/)
To run it locally, please setup the google app engine (python) follows [this](https://cloud.google.com/appengine/downloads) and navigate to the fullstackUdacity
folder and run:

```dev_appserver.py blog```

##TODO
* update the front-end to make it more beautiful and responsive
* ```time.sleep(.5)``` is used currently used to wait for the database update response to the browser, fix this with when update the front end.


##Copyright
The MIT License (MIT)
Copyright (c) <2016> \<Wenchen Li\>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
