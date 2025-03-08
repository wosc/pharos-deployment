#!/bin/bash

set -e

name=$1

cp client.conf $name.ovpn
echo '<ca>' >> $name.ovpn
sed -n '/BEGIN CERTIFICATE/,/END CERTIFICATE/p' < rsa/pki/ca.crt >> $name.ovpn
echo '</ca>' >> $name.ovpn
echo '<cert>' >> $name.ovpn
sed -n '/BEGIN CERTIFICATE/,/END CERTIFICATE/p' < rsa/pki/issued/$name.crt >> $name.ovpn
echo '</cert>' >> $name.ovpn
echo '<key>' >> $name.ovpn
sed -n '/BEGIN PRIVATE KEY/,/END PRIVATE KEY/p' < rsa/pki/private/$name.key >> $name.ovpn
echo '</key>' >> $name.ovpn
echo '<tls-auth>' >> $name.ovpn
sed -n '/BEGIN OpenVPN Static key V1/,/END OpenVPN Static key V1/p' < rsa/pki/ta.key >> $name.ovpn
echo '</tls-auth>' >> $name.ovpn
