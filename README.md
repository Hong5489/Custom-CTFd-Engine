# Custom CTFd engine
## Features
- Flag Sharing Prevention
- Dynamic Flag for Web Challenges and Binary Challenges

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
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Presstest Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nYivN04w.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Press Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nRivN04w.woff2) format('woff2');
  unicode-range: U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* greek */
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Press Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nWivN04w.woff2) format('woff2');
  unicode-range: U+0370-03FF;
}
/* latin-ext */
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Press Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nbivN04w.woff2) format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Press Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nVivM.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
html,
body,
.container {
  font-family: "Press Start 2P", "Press Start 2P", sans-serif;
  font-size: 0.9rem;
}
body{
background-color: #0c0d16;
color: #e4e2ff;
}

h1,
h2 {
  font-family: "Press Start 2P", "Press Start 2P", sans-serif;
  font-weight: 500;
  text-shadow: -1px 3px #222
  letter-spacing: 2px;
}
.btn{
  font-size: 0.75rem;
}
.h1,h1 {
    font-size: 2.25rem
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
.btn-outline-secondary{
border-color: #87c4f2;
}
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Press Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nYivN04w.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Press Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nRivN04w.woff2) format('woff2');
  unicode-range: U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* greek */
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Press Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nWivN04w.woff2) format('woff2');
  unicode-range: U+0370-03FF;
}
/* latin-ext */
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Press Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nbivN04w.woff2) format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Press Start 2P';
  font-style: normal;
  font-weight: 400;
  src: local('Press Start 2P Regular'), local('PressStart2P-Regular'), url(https://fonts.gstatic.com/s/pressstart2p/v7/e3t4euO8T-267oIAQAu6jDQyK3nVivM.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
html,
body,
.container {
  font-family: "Press Start 2P", "Press Start 2P", sans-serif;
  font-size: 0.9rem;
}
body{
background-color: #0c0d16;
color: #e4e2ff;
}

h1,
h2 {
  font-family: "Press Start 2P", "Press Start 2P", sans-serif;
  font-weight: 500;
  text-shadow: -2px 4px #222;
  letter-spacing: 2px;
}
.btn{
  font-size: 0.75rem;
}
.h1,h1 {
    font-size: 2.25rem
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
font-size: 125%;
border-radius: .2rem
}
code {
font-size: 125%;
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
```