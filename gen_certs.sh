#!/bin/sh

SSL_ROOT="ssl"
SUBJ="/CN=remote_launch"

mkdir -p $SSL_ROOT
rm $SSL_ROOT/*

openssl req \
  -x509 -nodes \
  -subj $SUBJ \
  -newkey rsa:2048 -keyout $SSL_ROOT/key.pem -out $SSL_ROOT/certificate.crt \
  2>/dev/null

openssl x509 -in $SSL_ROOT/certificate.crt -sha1 -noout -fingerprint