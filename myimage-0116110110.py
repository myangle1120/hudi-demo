from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow import DAG
from airflow.utils.dates import days_ago


from airflow.kubernetes.secret import Secret


args = {
    "project_id": "myimage-0116110110",
}

dag = DAG(
    "myimage-0116110110",
    default_args=args,
    schedule_interval="@once",
    start_date=days_ago(1),
    description="Created with Elyra 3.4.0 pipeline editor using `myimage.ipynb`.",
    is_paused_upon_creation=False,
)


# Ensure that the secret named 'my-s3-keys' is defined in the Kubernetes namespace where this pipeline will be run
env_var_secret_id = Secret(
    deploy_type="env",
    deploy_target="AWS_ACCESS_KEY_ID",
    secret="my-s3-keys",
    key="AWS_ACCESS_KEY_ID",
)
env_var_secret_key = Secret(
    deploy_type="env",
    deploy_target="AWS_SECRET_ACCESS_KEY",
    secret="my-s3-keys",
    key="AWS_SECRET_ACCESS_KEY",
)


# Operator source: myimage.ipynb
op_120e190e_59fb_4d0d_9854_381a7eb4949e = KubernetesPodOperator(
    name="myimage",
    namespace="default",
    image="harbor.dap.local/library/jdk:1.8",
    image_pull_secrets="my-s3-keys",
    cmds=["sh", "-c"],
    arguments=[
        "mkdir -p ./jupyter-work-dir/ && cd ./jupyter-work-dir/ && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.4.0/elyra/airflow/bootstrapper.py --output bootstrapper.py && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.4.0/etc/generic/requirements-elyra.txt --output requirements-elyra.txt && python3 -m pip install packaging && python3 -m pip freeze > requirements-current.txt && python3 bootstrapper.py --cos-endpoint http://172.16.221.218:19000 --cos-bucket spark-bucket --cos-directory 'myimage-0116110110' --cos-dependencies-archive 'myimage-120e190e-59fb-4d0d-9854-381a7eb4949e.tar.gz' --file 'myimage.ipynb' "
    ],
    task_id="myimage",
    env_vars={
        "runtime_platform": "APACHE_AIRFLOW",
        "ELYRA_RUNTIME_ENV": "airflow",
        "ELYRA_ENABLE_PIPELINE_INFO": "True",
        "ELYRA_RUN_NAME": "myimage-0116110110-{{ ts_nodash }}",
    },
    resources={
        "request_cpu": "1",
        "request_memory": "1",
    },
    secrets=[env_var_secret_id, env_var_secret_key],
    in_cluster=True,
    config_file="None",
    dag=dag,
)

op_120e190e_59fb_4d0d_9854_381a7eb4949e.image_pull_policy = "IfNotPresent"
