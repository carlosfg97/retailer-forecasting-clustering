
## Running the Store Cluster microservice with Docker Containers

![](https://icon-library.com/images/docker-icon/docker-icon-12.jpg) ![](https://pbs.twimg.com/profile_images/1366779897423810562/kn7ucNPv_400x400.png)


The solution requires to build and run 2 separate containers. The first one reads the input csv and generates clusters based on the complete dataset. The outputs are saved to a volume from where the second container will start. 

### First Container: model_app

* Create a folder that will work as a common volume between the two containers (this will be defined during the _docker run_). Download the dataset from [Kaggle]('https://www.kaggle.com/c/favorita-grocery-sales-forecasting/data') and copy our 2 inputs: `train.csv` and `items.csv` into the data folder (after unzipping them).
```
mkdir docker_data
mkdir docker_data/data
mkdir docker_data/outputs

# in the path where the download is:
cp train.csv <path to docker_data/data>
cp items.csv <path to docker_data/data>
```
* Take a note of the full path where you have created the __docker_data__ directory, since you will have to reference it later.

Once the folder is created, run the docker build and docker run commands. The parameter `-v` allows to define a shared channel between the container and the host's storage system in the form of 
`local_path:container_path`. Notice we are using the local path where the inputs train.csv and items.csv were copied to in the previous step.

Make sure to run the following while standing in __model_app__ folder in the repo:
```
docker build -t model_app .

docker run -v C:\Users\carlo\docker_data:/docker_data model_app
```

This first container will run Python scripts, write outputs in CSV and PKL formats into the volume and shut down once finished.

### Second Container: streamlit_app

Now the second docker will also use the previosuly defined path as volume access and fetch the files created in the previous step. In this second container we also need to use the parameter `-p` to link the exposed port in the container to the same port in our local machines (`8501:8501`)

```
docker build -t streamlit_app . 

docker run --name clusters_app -v C:\Users\carlo\docker_data:/docker_data -p 8501:8501 streamlit_app
```

If you need to build the container again (in case you have done changes to the streamlit app code) but the port is taken by the old one, you can "kill" the previous one by:

```
docker container ls # to confirm the container is still running

docker rm -f clusters_app 
```

If you just want to stop the container and start it again later:
```
docker stop clusters_app
docker start clusters_app
```
