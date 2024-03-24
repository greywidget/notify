# Notify
Checks various internet sites and notify me via [ntfy](https://ntfy.sh) of anything of interest.

# On dealing with Amazon
When I first encountered a message from Amazon: *Looks like you are a program...*
I assumed I needed to use PlayWright rather than Requests to access
the site. This caused me to create a [PlayWright Version](https://github.com/greywidget/notifypw)  
Later, I modded *this* version and added a `USER_AGENT` to the request header. 
This seemed to be working for a few days and then I started getting the error
again. It appears to be intermittent and perhaps the PlayWright version is the
best solution for now.  
Unfortunately the Docker Image for the PlayWright version is about 1.22 GB
compared to the Docker Image for this which is 110 MB. And if you install
all PlayWright Browsers `playwright install --with-deps` instead of just one
`playwright install --with-deps chromium`, the Docker Image is over 2 GB.

# I did make a package version

I did create a version of this as a package [Hatch Notify](https://github.com/greywidget/hatch-notify), but on reflection it was not a great idea and gave me issues using `python-decouple` that I couldn't resolve, and I ended up adding the TOPIC directly as an environmental variable.

# Docker
I put the Docker files in this repo for reference, so they will get
pulled down when you clone the repo. However they need to be in the
install directory for when you run `docker-compose`.  
Note that I had issues with `startup.sh` because my `Windows Git`
changed the line endings (to CRLF) and `sh` on Synology doesn't
like that.  
My workaround was to edit the files on Synology with the `Text Edit` package to reset the line endings.
