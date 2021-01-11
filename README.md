# Custom CTFd engine
Custom made CTFd engine by SKR, live at [skrctf.me](skrctf.me). Upgraded to Python3!

## Features
- Flag Sharing Prevention
- Dynamic Flag for Web Challenges and Binary Challenges
- Web Shell login using Team Credentials
- Reverse Proxy for Web Challenges
- Arrange category priority
- Arrange challenges by difficulty
- Discord bot announce challenges
- Netcat container for multiple challenges

First run this:
```
pip install -r requirements.txt
```
Then install `docker` and `docker-compose` (For Debian):
```
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
echo 'deb https://download.docker.com/linux/debian stretch stable' > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install docker-ce
pip install docker-compose
```

After that, run this and you're done!
```
docker-compose up
```

## Themes
### 8 bit Theme

Go to /admin/config, enter the following code to Stylesheet editor and press **Update**:
```css
html,
body,
.container {
  font-family: "Volter", "Volter", sans-serif;
}
body{
background-color: #0c0d16;
color: #e4e2ff;
}

h1{
  font-family: "fuck", "fuck", sans-serif;
}
h2{
 font-family: "Volter", "Volter", sans-serif;
}
.btn{
  font-size: 0.85rem;
}
.h1,h1 {
    font-size: 4.25rem
}

.h2,h2 {
    font-size: 1.75rem
}
a {
color: #714cdf;
text-decoration: none;
background-color: transparent
}

a:hover {
color: #4922bd;
text-decoration: underline
}
.modal-content{
background-color: #32334a;
}
.btn-info {
    background-color: #714cdf !important;
    border-color: #714cdf !important;
}
.btn-outline-secondary {
color: #17b06b;
border-color: #17b06b
}

.btn-outline-secondary:hover {
color: #fff;
background-color: #17b06b;
border-color: #17b06b
}
.btn-outline-secondary.focus, .btn-outline-secondary:focus {
-webkit-box-shadow: 0 0 0 .2rem rgba(23, 176, 107, .5);
box-shadow: 0 0 0 .2rem rgba(23, 176, 107, .5)
}
kbd {
padding: .2rem .4rem;
font-size: 100%;
border-radius: .2rem
}
code {
font-size: 100%;
color: #17b06b;
}
.solved-challenge {
    opacity: 1;
}

.form-control:focus {
    background-color: transparent;
    border-color: #a3d39c;
    box-shadow: 0 0 0 0.2rem #a3d39c;
    transition: background-color 0.3s, border-color 0.3s;
    color: white;
}
/* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #17b06b;
}

input:focus + .slider {
  box-shadow: 0 0 1px #17b06b;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

.card{
  background-color:transparent;
  border:4px solid #fff;
}

.nav-pills .nav-link.active, .nav-pills .show>.nav-link{
  background-color:transparent;
  border: 2px solid #37d63e;
  border-radius: 0;
}
```
