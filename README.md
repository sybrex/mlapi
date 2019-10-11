# Machine Learning API

[API docs](http://ml.viktors.info/docs)

## Projects

### Klitschko brothers image classifier
Predict who of two brothers is on the photo

### Odds Generator 

The are multiple markets you can bet on sports events. But there are several markets which could be used to generate other markets.
Based on these main markets: Match Result Full Time (MRFT), Over/Under Full Time 2.5(OUFT) and Both Teams to Score (BTS) we are going to generate other markets e.g Double Chance Full Time (DCFT), Match Result Half Time (MRHT) or Match Result Second Half (MRSH)

## Technical details

### Running uvicorn as a systemd service

Edit /etc/systemd/system/mlapi.uvicorn.service
```
[Unit]
Description=uvicorn server for machine learning api
After=network.target

[Service]
User=viktor
Group=nginx
ExecStart=/var/www/vhosts/mlapi/uvicorn.sh
```

Start the service
```
sudo service klitschko.uvicorn.service start
```

### Running behind nginx

Edit /etc/nginx/conf.d/ml.viktors.info.conf
```
server {
    listen 80;
    client_max_body_size 4G;

    server_name ml.viktors.info;

    location / {
      proxy_set_header Host $http_host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_redirect off;
      proxy_buffering off;
      proxy_pass http://localhost:8000;
    }
}
upstream uvicorn {
    server unix:/tmp/uvicorn.sock;
}
```

### Examples

* [Klitshchko image classifier](https://viktors.info/labs/klitschko)
* [Sports odds generator](https://viktors.info/labs/markets)


### Resources

* [Practical Deep Learning for Coders, v3](https://course.fast.ai/)
* [Starlette framework](https://www.starlette.io/)
* [FastAPI framework](https://fastapi.tiangolo.com/)
* [How (and why) to create a good validation set](https://www.fast.ai/2017/11/13/validation-sets/)
* [Tips for building large image datasets](https://forums.fast.ai/t/tips-for-building-large-image-datasets/26688)
* [Cougar or not by Simon Willison](https://github.com/simonw/cougar-or-not)
* [systemd](https://www.freedesktop.org/wiki/Software/systemd/)