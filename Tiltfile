APP_NAME = "surfersweb"
SOURCE_IMAGE = os.getenv("SOURCE_IMAGE", default='harbor.services.tanzu.rocks/tap3/supply-chain/surfersweb-source')
LOCAL_PATH = os.getenv("LOCAL_PATH", default='.')
NAMESPACE = os.getenv("NAMESPACE", default='default')
K8S_CONTEXT = os.getenv("K8S_CONTEXT", default="tap-aus-3")
WORKLOAD_FILE = "config/surfersweb-workload-db.yaml"

k8s_custom_deploy(
    APP_NAME,
    apply_cmd="tanzu apps workload apply -f " + WORKLOAD_FILE + " --live-update" +
               " --local-path " + LOCAL_PATH +
               " --source-image " + SOURCE_IMAGE +
               " --namespace " + NAMESPACE +
               " --yes >/dev/null" +
               " && kubectl get workload " + APP_NAME + " --namespace " + NAMESPACE + " -o yaml",
    delete_cmd="tanzu apps workload delete -f " + WORKLOAD_FILE + " --namespace " + NAMESPACE + " --yes",
    deps=['app.py'],
    container_selector='workload',
    live_update=[
      sync('.', '/workspace')
    ]
)

k8s_resource(APP_NAME, port_forwards=["8080"],
            extra_pod_selectors=[{'serving.knative.dev/service': APP_NAME}])

allow_k8s_contexts(K8S_CONTEXT)

update_settings ( 
    max_parallel_updates = 3 , 
    k8s_upsert_timeout_secs = 600 , 
    suppress_unused_image_warnings = None 
)

