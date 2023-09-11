 
 appBasePath=/home/admin/myapps/ledpython/
 appLogsPath=${appBasePath}/logs/
 appUploadPath=${appBasePath}/upload/
 mkdir ${appBasePath}
 mkdir ${appLogsPath}
 mkdir ${appUploadPath}
 
 docker container run -d \
        --name led_flask -p 1238:18080 \
        --volume "$PWD/":/app  \
        --volume "${appLogsPath}/":/app/logs  \
        --volume "${appUploadPath}/":/app/upload  \
        python /bin/bash -c "chmod +x /app/docker_run.sh;/app/docker_run.sh"