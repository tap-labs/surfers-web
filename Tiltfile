SOURCE_IMAGE = os.getenv("SOURCE_IMAGE", default='us.gcr.io/lloyd-266015/supply-chain/surferslookout-alpha')
LOCAL_PATH = os.getenv("LOCAL_PATH", default='.')
NAMESPACE = os.getenv("NAMESPACE", default='alpha')
APP_NAME = "surferslookout"
K8S_CONTEXT = os.getenv("K8S_CONTEXT", default="tap-aus-2")

k8s_custom_deploy(
    APP_NAME,
    apply_cmd="tanzu apps workload apply -f tap/config/workload.yaml --live-update" +
               " --local-path " + LOCAL_PATH +
               " --source-image " + SOURCE_IMAGE +
               " --namespace " + NAMESPACE +
               " --yes >/dev/null" +
               " && kubectl get workload " + APP_NAME + " --namespace " + NAMESPACE + " -o yaml",
    delete_cmd="tanzu apps workload delete -f tap/config/workload.yaml --namespace " + NAMESPACE + " --yes",
    deps=['app.py'],
    container_selector='workload',
    live_update=[
      sync('.', '/workspace')
    ]
)

k8s_resource(APP_NAME, port_forwards=["80:80"],
            extra_pod_selectors=[{'serving.knative.dev/service': APP_NAME}])

allow_k8s_contexts(K8S_CONTEXT)