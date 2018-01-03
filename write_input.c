#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <linux/input.h>

#define ABS_MT_SLOT     0x2f    /* MT slot being modified */
#define ABS_MT_TOUCH_MAJOR  0x30    /* Major axis of touching ellipse */
#define ABS_MT_TOUCH_MINOR  0x31    /* Minor axis (omit if circular) */
#define ABS_MT_WIDTH_MAJOR  0x32    /* Major axis of approaching ellipse */
#define ABS_MT_WIDTH_MINOR  0x33    /* Minor axis (omit if circular) */
#define ABS_MT_ORIENTATION  0x34    /* Ellipse orientation */
#define ABS_MT_POSITION_X   0x35    /* Center X touch position */
#define ABS_MT_POSITION_Y   0x36    /* Center Y touch position */
#define ABS_MT_TOOL_TYPE    0x37    /* Type of touching device */
#define ABS_MT_BLOB_ID      0x38    /* Group a set of packets as a blob */
#define ABS_MT_TRACKING_ID  0x39    /* Unique ID of initiated contact */
#define ABS_MT_PRESSURE     0x3a    /* Pressure on contact area */
#define ABS_MT_DISTANCE     0x3b    /* Contact hover distance */
#define ABS_MT_TOOL_X       0x3c    /* Center X tool position */
#define ABS_MT_TOOL_Y       0x3d    /* Center Y tool position */

int mt_fd;

int write_event(unsigned short type, unsigned short code, int value)
{
    struct input_event mt_event;
    mt_event.type=type;
    mt_event.code=code;
    mt_event.value=value;
    gettimeofday(&mt_event.time,0);
    write(mt_fd,&mt_event,sizeof(mt_event));
    return 0;
}

int write_mt_event(unsigned short code, int value)
{
    return write_event(EV_ABS,code,value);
}

int write_sync_event()
{
    return write_event(0,0,0);
}

int main(int argc, char **argv)
{
    int usleep_second;
    if(argc < 2){
        usleep_second = 0;
    }
    else{
        usleep_second = atoi(argv[1]);
    }

    mt_fd = open("/dev/input/event2",O_RDWR);
    if(mt_fd <0) {
        fprintf(stderr,"open input device failed\n");
        exit(mt_fd);
    }

    write_mt_event(ABS_MT_TRACKING_ID,0x188);
    write_mt_event(ABS_MT_POSITION_X,0x146);
    write_mt_event(ABS_MT_POSITION_Y,0x40b);
    write_mt_event(ABS_MT_WIDTH_MAJOR,0xf);
    write_mt_event(ABS_MT_TOUCH_MAJOR,0xb);
    write_mt_event(ABS_MT_TOUCH_MINOR,0x7);
    write_sync_event();
    usleep(usleep_second);
    write_mt_event(ABS_MT_TRACKING_ID,-1);
    write_sync_event();
    return 0;
}
