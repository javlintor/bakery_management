Public IP -> 15.237.184.37

# Only first time

- generate secret key

```python
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_secret_key())"
```

- create .env
- migrate
- create super user
- db seed
- collect staticfiles
- Bread images
- create a `/etc/systemd/system/gunicron.service` file.

```
[Unit]
Description=Gunicorn daemon for Django app
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/srv/app/manolibakes
EnvironmentFile=/srv/app/.env
ExecStart=/srv/app/.venv/bin/gunicorn \
        --workers 3 \
        --bind unix:/srv/app/gunicorn.sock \
        manolibakes.wsgi:application

[Install]
WantedBy=multi-user.target
```

- Create a config file for nginx at `/etc/nginx/conf.d/app.conf`

```
server {
        listen 80;
        server_name _;

        location /static/ {
                alias /srv/app/staticfiles/;
        }

        location / {
                proxy_pass http://unix:/srv/app/gunicorn.sock;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```

# Every deployment

- sync code with something like

```
 rsync -avz --exclude '__pycache__' --exclude '.env' --exclude 'data' --exclude '.venv' --exclude
 '*.pyc' ./ ec2-user@15.237.184.37:/srv/app
```

Then restart gunicorn service in the server

```
sudo systemctl restart gunicorn.service
```
