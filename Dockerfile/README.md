This dockerfile is for standalone mercury pod. The thought process here is to have basic setup of Python3.9 and then install mercury with its dependencies. and run `mercury run 0.0.0.0:9000` on start. This approach worked for me. 
  
We can customise this docker file by adding all the extra libraries which was used by notebooks.