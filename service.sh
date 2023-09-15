#!/bin/bash
#chkconfig: 2345 80 40
#description: DESCRIPTION
#pidfile:/var/run/DEFAULT_SEVICE_NAME.pid

SYS_PATH=/etc/init.d
SEVICE_NAME=DEFAULT_SEVICE_NAME
EXE_PATH=DEFAULT_EXE_PATH
EXE_NAME=DEFAULT_EXE_NAME
PID_FILE=/var/run/DEFAULT_SEVICE_NAME.pid
CORE_LIMIT_NUM=3

#$1 service name , $2 exe name
Install()
{
    if [ -z "$1" ];then
        echo "please input parame1:service name."
        return 1
    fi
    if [ -z "$2" ];then
        echo "please input parame1:exe name."
        return 1
    fi
    if [ ! -d $SYS_PATH ];then
        mkdir -p $SYS_PATH
        chmod 777 $SYS_PATH
    fi

    SEVICE_NAME=$1
    EXE_NAME=$2
    EXE_PATH=`pwd`
    if [ ! -f $EXE_PATH/$EXE_NAME ]; then
        echo "$EXE_PATH/$EXE_NAME not exist"
        return 1
    fi    
#set suid_dumpable
    if [ -e /proc/sys/kernel/suid_dumpable ]; then
        echo 1 > /proc/sys/kernel/suid_dumpable
    else
        echo 1 > /proc/sys/fs/suid_dumpable
    fi
#set core dump dir
    echo 'core-%e-%p-%t'  > /proc/sys/kernel/core_pattern
    ulimit -c unlimited
#copy self to /etc/init.d
    sed  -e "s%DEFAULT_SEVICE_NAME%$SEVICE_NAME%g"  \
        -e "s%DEFAULT_EXE_PATH%$EXE_PATH%g"\
        -e "s%DEFAULT_EXE_NAME%$EXE_NAME%g" $0 > $SYS_PATH/$SEVICE_NAME
    
    chmod 755 $SYS_PATH/$SEVICE_NAME
    chmod 755 $EXE_PATH/$EXE_NAME
    if [ -f /etc/init.d/functions ]; then
        chkconfig --add $SEVICE_NAME
    elif [ -f /lib/lsb/init-functions ];then
        update-rc.d $SEVICE_NAME defaults
    else
        echo "unrecognized sysv command"
        return 1
    fi    
    systemctl daemon-reload
    echo "install $SEVICE_NAME service succ"
    return 0
}

Uninstall()
{
    if [ -z "$1" ];then
        echo "please input parame1:service name."
        return 1
    fi
    SEVICE_NAME=$1
    if [ ! -f $SYS_PATH/$SEVICE_NAME ]; then
        echo     "$SYS_PATH/$SEVICE_NAME not exist"
    fi
    
    if [ -f /etc/init.d/functions ]; then
        chkconfig --del $SEVICE_NAME
    elif [ -f /lib/lsb/init-functions ];then
        update-rc.d $SEVICE_NAME remove
    else
        echo "unrecognized sysv command"
        return 1
    fi
    rm -f $SYS_PATH/$SEVICE_NAME
    systemctl daemon-reload
    echo "uninstall $SEVICE_NAME service succ"
    return 0
}

Start()
{
    cd $EXE_PATH
#rm more core_dump file
    COUNT=1
    corefiles=`ls -t core-$EXE_NAME-*`
    for file in $corefiles
    do
        if [ $COUNT -gt $CORE_LIMIT_NUM ];then
            rm -rf $file
        fi
        let COUNT=$COUNT+1
    done
    
    if [ -f $PID_FILE ]; then
        echo "$SEVICE_NAME already running"    
        return 1
    fi
    ulimit -c unlimited
#start exe
    $EXE_PATH/$EXE_NAME &
    pid=`ps -ef|grep $EXE_PATH/$EXE_NAME|grep -v 'grep'|awk '{print $2}'`
    if [ -z $pid ]; then
        echo "$EXE_PATH/$EXE_NAME exec failed"
        return 1
    fi
    touch $PID_FILE
    echo $pid > $PID_FILE
    if [ $? -eq 0 ]; then
        echo "start $SEVICE_NAME service succ"
        return 0
    else
        echo "start $SEVICE_NAME service failed"
        return -1    
    fi
}

Stop()
{
    if [ ! -f $PID_FILE ]; then
        echo "$SEVICE_NAME not running"
        return 1    
    fi
    pid=`cat $PID_FILE`
    if [ -z $pid ]; then
        rm -rf $PID_FILE
        echo "$SEVICE_NAME not running"
        return 1
    fi
    kill $pid
    if [ $? -eq 0 ];then
        rm -rf $PID_FILE
        echo "stop $SEVICE_NAME service succ"
        return 0
    else
        echo "stop $SEVICE_NAME service failed"
        return 1    
    fi        
}
RETVAL=0
case $1 in
    install)
        Install $2 $3
        RETVAL=$?
        ;;
    uninstall)
        Uninstall $2
        RETVAL=$?
        ;;
    start)
        echo "enter Start"
        Start
        RETVAL=$?
        ;;
    stop)
        echo "enter Stop"
        Stop
        RETVAL=$?
        ;;        
esac
exit $RETVAL