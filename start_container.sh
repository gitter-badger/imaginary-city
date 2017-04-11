docker run -p 8080:80 \
           -ti \
           -v "$(pwd)":/home/imgcity/server \
           imaginary-city-env \
           /bin/bash
