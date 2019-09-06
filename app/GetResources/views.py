# Django
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Kubernetes.
from kubernetes import client, config
# Others.
import os
import logging
import re

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

logger=logging.getLogger("__name__")

@method_decorator(csrf_exempt, name='dispatch')
class GetPods(View):
  def get(self, request):
    """
    Returns information about a specific pod or pods based on the search criteria.    
    GET /getpods?name=$NAME&namespace=$NAMESPACE
    Headers:
      - Authorization: Bearer $TOKEN
    """
    logger.info("Endpoint getpods hit.")
    # Get request parameter.
    name_search_parameter:str=request.GET.get("name", "")
    namespace_parameter:str=request.GET.get("namespace", "")
    # Get headers.
    authorization_token=request.headers['Authorization']
    authorization_token=re.findall("Bearer (.*)", authorization_token)[0]
    # Env variables inside pod.
    kubernetes_svc:str=os.environ["KUBERNETES_SERVICE_HOST"]
    # Load kubernetes config.
    configuration:any=client.Configuration()
    configuration.api_key["authorization"]=authorization_token
    configuration.api_key_prefix["authorization"]="Bearer"
    configuration.host:str="https://"+kubernetes_svc
    configuration.ssl_ca_cert:str="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
    logger.debug("Name param: "+name_search_parameter)
    #print("DEBUG: token: ", authorization_token)
    logger.debug("Namespace: "+namespace_parameter)
    logger.debug("k8s service host: "+kubernetes_svc)
    v1 = client.CoreV1Api(client.ApiClient(configuration))
    try:
      pods=v1.list_namespaced_pod(namespace_parameter)
    except:
      logger.error("k8s api")
    # Logic to find the pod.
    matched_pods:list=[]
    for index_i, pod in enumerate(pods.items):
      #print("DEBUG: ", pod)
      pod_name:str=pod.metadata.name
      print("DEBUG: Pod name: ", pod_name)
      containers:any=pod.spec.containers[:]
      phmap:dict={}
      if len(re.findall(name_search_parameter, pod_name)) > 0:
        containers_list:list=[]
        if len(containers) > 0:
          for index_j, container in enumerate(containers):
            chmap:dict={}
            container_name:str=container.name
            container_env_vars:list=container.env
            print("DEBUG: Container name: ", container_name)
            env_vars_list:list=[]
            if container_env_vars is not None:
              for index_k, env_var in enumerate(container_env_vars):
                ehmap:dict={}
                env_var_name:str=env_var.name
                env_var_value:str=env_var.value
                ehmap["name"]=env_var_name
                ehmap["value"]=env_var_value
                env_vars_list.append(ehmap)
            chmap["name"]=container_name
            chmap["env"]=env_vars_list
            containers_list.append(chmap)
        phmap["name"]=pod_name
        phmap["containers"]=containers_list
        matched_pods.append(phmap)
    response:dict={'matched_pods': matched_pods}
    print("DEBUG: reponse: ", response)
    # Return json response.
    return JsonResponse(response, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class GetServices(View):
  def get(self, request):
    """
    Returns information about a specific pod or pods based on the search criteria.
    GET /getservices?name=$NAME&namespace=$NAMESPACE
    Headers:
      - Authorization: Bearer $TOKEN
    """
    pass

  def post(self):
    """
    :return:
    """
    pass