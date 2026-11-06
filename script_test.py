sudo systemctl daemon-reload
sudo systemctl enable blindscript.service
sudo systemctl start blindscript.service

to check status

sudo systemctl status blindscript.service

journalctl -u your_service_name.service -f
