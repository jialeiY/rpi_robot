export LD_PRELOAD=/usr/lib/uv4l/uv4lext/armv6l/libuv4lext.so;


ffserver -f ffserver.conf &
 ffmpeg -s 320x240  \
 -f video4linux2 -i /dev/video0 \
-r 5  http://localhost:8090/feed1.ffm
