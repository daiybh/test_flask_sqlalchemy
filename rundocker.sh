 
 appBasePath=/home/admin/myapps/ledpython/
 appLogsPath=${appBasePath}/logs/
 appUploadPath=${appBasePath}/upload/
 #mkdir ${appBasePath}
 #mkdir ${appLogsPath}
 #mkdir ${appUploadPath}
 ln -s ${appBasePath} $PWD
 

 docker container run -d \
        --name led_flask -p 1238:18080 \
        --volume "$PWD/":"/home/admin/myapps/ledpython/"  \
        python /bin/bash -c "chmod +x /home/admin/myapps/ledpython/docker_run.sh;/home/admin/myapps/ledpython/docker_run.sh"