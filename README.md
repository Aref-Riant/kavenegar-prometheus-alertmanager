# kavenegar-prometheus-alertmanager
prometheus alertmanager webhook sms gateway for kavenegar

# requirements:
python3
pip3
kavenegar ( pip3 install kavenegar )

this python program listens on 'listen_on' port as a webhook to recieve json alert data from prometheus alert manager
then groups the alerts and sends them to [kavenegar](https://kavenegar.com)(iranian sms service provider) sms api.

