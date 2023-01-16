from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow import DAG
from airflow.utils.dates import days_ago


from airflow.kubernetes.secret import Secret


args = {
    "project_id": "mulaf1-0116104347",
}

dag = DAG(
    "mulaf1-0116104347",
    default_args=args,
    schedule_interval="@once",
    start_date=days_ago(1),
    description="Created with Elyra 3.4.0 pipeline editor using `mulaf1.pipeline`.",
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


# Operator source: note1.ipynb
op_021ece5c_40d2_4951_a8d9_bd0932109195 = KubernetesPodOperator(
    name="note1",
    namespace="default",
    image="amancevice/pandas:1.1.1",
    cmds=["sh", "-c"],
    arguments=[
        "mkdir -p ./jupyter-work-dir/ && cd ./jupyter-work-dir/ && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.4.0/elyra/airflow/bootstrapper.py --output bootstrapper.py && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.4.0/etc/generic/requirements-elyra.txt --output requirements-elyra.txt && python3 -m pip install packaging && python3 -m pip freeze > requirements-current.txt && python3 bootstrapper.py --cos-endpoint http://172.16.221.218:19000 --cos-bucket spark-bucket --cos-directory 'mulaf1-0116104347' --cos-dependencies-archive 'note1-021ece5c-40d2-4951-a8d9-bd0932109195.tar.gz' --file 'note1.ipynb' "
    ],
    task_id="note1",
    env_vars={
        "ELYRA_RUNTIME_ENV": "airflow",
        "ELYRA_ENABLE_PIPELINE_INFO": "True",
        "ELYRA_RUN_NAME": "mulaf1-0116104347-{{ ts_nodash }}",
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


# Operator source: {'catalog_type': 'elyra-airflow-examples-catalog', 'component_ref': {'component-id': 'bash_operator.py'}}
op_e7a97fea_dbc9_431b_bd6a_f5ca6dad5c35 = BashOperator(
    task_id="BashOperator",
    bash_command="",
    xcom_push=True,
    env={},
    output_encoding="utf-8",
    dag=dag,
)

op_e7a97fea_dbc9_431b_bd6a_f5ca6dad5c35 << op_021ece5c_40d2_4951_a8d9_bd0932109195


# Operator source: py1.py
op_66359380_fc0d_48ea_bf08_99758ef65a5e = KubernetesPodOperator(
    name="py1",
    namespace="default",
    image="continuumio/anaconda3:2020.07",
    cmds=["sh", "-c"],
    arguments=[
        "mkdir -p ./jupyter-work-dir/ && cd ./jupyter-work-dir/ && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.4.0/elyra/airflow/bootstrapper.py --output bootstrapper.py && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.4.0/etc/generic/requirements-elyra.txt --output requirements-elyra.txt && python3 -m pip install packaging && python3 -m pip freeze > requirements-current.txt && python3 bootstrapper.py --cos-endpoint http://172.16.221.218:19000 --cos-bucket spark-bucket --cos-directory 'mulaf1-0116104347' --cos-dependencies-archive 'py1-66359380-fc0d-48ea-bf08-99758ef65a5e.tar.gz' --file 'py1.py' "
    ],
    task_id="py1",
    env_vars={
        "ELYRA_RUNTIME_ENV": "airflow",
        "ELYRA_ENABLE_PIPELINE_INFO": "True",
        "ELYRA_RUN_NAME": "mulaf1-0116104347-{{ ts_nodash }}",
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

op_66359380_fc0d_48ea_bf08_99758ef65a5e << op_021ece5c_40d2_4951_a8d9_bd0932109195
