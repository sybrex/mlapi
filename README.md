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

## Configure 