## How to build an environment when your Azure ML workspace is behind a VNet

1. Create a folder for you docker context called 'DockerContext'
2. In 'DockerContext' folder create a 'requirements.txt' file that contains your  packages:  
```
        openpyxl==3.0.10   
        pyod==1.0.4    
        kaleido==0.2.1  
        plotly==5.10.0    
        pandas==1.1.5    
        numpy==1.21.6    
        seaborn==0.11.2    
        pathlib2==2.3.7.post1    
        matplotlib==3.2.1    
        argparse    
```
It’s a good practice to fix the versions. You can find the version with command: ``pip freeze | grep 'the package name' ``  

3.	Create a Dockerfile:  
```        
        #FROM mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04
        FROM python:3.8

        # python installs
        COPY requirements.txt .
        RUN pip install -r requirements.txt

        # set command
        CMD ["bash"]
```

Note: You can use a base image or create an environment from scratch.
In case you want to use one already deployed to ACR environment - 'Golden Image', you can point in the the Dockerfile to it, and add only the dependencies that you are missing in the  'requirements.txt' (Look at DockerContextAdd folder). 

4. Open terminal in your 'DockerContext' folder 

5.	Login to your ACR:  
``  
    docker login your-acr-name.azurecr.io  
``  
You will find the username (it's your-acr-name) and the password in the Access keys section of your ACR.  

6.	Build your docker file locally:

    ``docker image build -t your-acr-name.azurecr.io/repo/mynewenv:v1 .
    `` 
7.	Push your image to ACR:  

    ``docker push your-acr-name.azurecr.io/repo/mynewenv:v1
``  
8.	Point your job/component environment to the new image:   
``   image: your-acr-name.azurecr.io/repo/ mynewenv:v1
    ``  
