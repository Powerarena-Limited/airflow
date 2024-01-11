import unittest
from unittest.mock import patch, MagicMock
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

class TestK8sExecutor(unittest.TestCase):
    @patch.object(KubernetesPodOperator, "__init__", return_value=None)
    @patch.object(BashOperator, "__init__", return_value=None)
    def test_tasks(self, mock_k8s_init, mock_bash_init):
        # Mock the DAG
        dag = MagicMock()

        # Call the tasks with the mocked operators
        task_hello = KubernetesPodOperator(
            task_id='hello_task',
            name='hello-pod',
            image='busybox',
            cmds=['sh', '-c', 'time sleep 60'],
            namespace='airflow',
            dag=dag,
        )

        bash_task = BashOperator(
            task_id='run_bash_command',
            bash_command='echo "Hello, Airflow?! 60"',
            dag=dag,
        )

        # Assert that the operators were called with the correct arguments
        mock_k8s_init.assert_called_with(
            task_id='hello_task',
            name='hello-pod',
            image='busybox',
            cmds=['sh', '-c', 'time sleep 60'],
            namespace='airflow',
            dag=dag,
        )
        mock_bash_init.assert_called_with(
            task_id='run_bash_command',
            bash_command='echo "Hello, Airflow?! 60"',
            dag=dag,
        )
        
if __name__ == '__main__':
    unittest.main()