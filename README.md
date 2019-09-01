# API

## Running uvicorn as a systemd service

Edit /etc/systemd/system/klitschko.uvicorn.service
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

## Running behind nginx

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

## Example

<a href="https://viktors.info/labs/klitschko" target="_blank">Demo</a>