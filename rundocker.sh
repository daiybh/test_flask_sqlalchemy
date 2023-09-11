 
 appBasePath=/home/admin/myapps/ledpython/
 appLogsPath=${appBasePath}/logs/
 appUploadPath=${appBasePath}/upload/
 #mkdir ${appBasePath}
 #mkdir ${appLogsPath}
 #mkdir ${appUploadPath}
 ln -s $PWD ${appBasePath} 


 docker container run -d \
        --name led_flask -p 1238:18080 \
        --volume "$PWD/":"/home/admin/myapps/ledpython/"  \
        python /bin/bash -c "cd /home/admin/myapps/ledpython/;chmod +x docker_run.sh;./docker_run.sh"