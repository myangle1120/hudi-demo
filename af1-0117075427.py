from airflow.operators.bash_operator import BashOperator
from airflow import DAG
from airflow.utils.dates import days_ago


from airflow.kubernetes.secret import Secret


args = {
    "project_id": "af1-0117075427",
}

dag = DAG(
    "af1-0117075427",
    default_args=args,
    schedule_interval="@once",
    start_date=days_ago(1),
    description="Created with Elyra 3.4.0 pipeline editor using `af1.pipeline`.",
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


# Operator source: {'catalog_type': 'elyra-airflow-examples-catalog', 'component_ref': {'component-id': 'bash_operator.py'}}
op_50b32fba_d049_494c_a523_0ab9dee82aad = BashOperator(
    task_id="shell",
    bash_command='echo "wo de airflow project"',
    xcom_push=True,
    env={},
    output_encoding="utf-8",
    dag=dag,
)
