fabric:
  forward_ssh_agent: 1
  colorize_errors: 1
  hosts:
    - localhost

stages:
  default: pi-tank-m1
  pi-tank-m1:
    hosts:
      - pi-tank-m1
    user: pi
    password:
  wlan:
    hosts:
      - 192.168.188.30
    user: pi
    password:

services:
  webiopi:
    port: 8083

  picam:
    fps: 7
    res: '320x240'
    port: 8081
    led: 'off'

  piserver:
    port: 8000

  pisound:
    timeout: 10                # network timeout in seconds (floats allowed), default: None
    idletimeout:               # timeout for fetching the result of the idle command is handled seperately, default: None
    host: 0.0.0.0            #mpd server
    port: 6600                 #mpd server port
    web: 8091

  pimpd:
    host: 0.0.0.0
    port: 6600

  udhcpd: file:config/udhcpd.yml
  nat: file:config/nat.yml
  lan: file:config/lan.yml
  accesspoint: file:config/accesspoint.yml
  wlan: file:config/wlan.yml
  hostapd: file:config/hostapd.yml
