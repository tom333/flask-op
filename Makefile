run:
	gunicorn "flask_op.flask_op:create_app('config.py')" -b :8000 --certfile keys/local.crt --keyfile keys/local.key --reload


generate-keys:
	openssl genrsa -des3 -out keys/rootCA.key 4096
	openssl req -x509 -new -nodes -key keys/rootCA.key -sha256 -days 1024 -out keys/rootCA.crt
	openssl genrsa -out keys/local.key 2048
	openssl req -new -sha256 -key keys/local.key -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=local" -out keys/local.csr
	openssl x509 -req -in keys/local.csr -CA keys/rootCA.crt -CAkey keys/rootCA.key -CAcreateserial -out keys/local.crt -days 5000 -sha256
	sudo cp rootCA.crt /usr/local/share/ca-certificates
	sudo update-ca-certificates
	#Clé utilisée pour signer les jwt
	openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout keys/signing_key.pem -out keys/signing_key.pem


docker-image:
	docker build -t flask_op:latest -f docker/Dockerfile .

clean:
	find . -name "__pychache__" -exec rm -Rf {} \;
	find . -name "*.pyc" -exec rm -f {} \;