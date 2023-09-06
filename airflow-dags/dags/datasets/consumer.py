from airflow.decorators import dag, task
from airflow import Dataset
from datetime import datetime

data_a = Dataset("s3://bucket_a/data_a")
data_b = Dataset("s3://bucket_b/data_b")

@dag(start_date=datetime(2023, 1 ,1), schedule=[data_a, data_b], catchup=False)
def consumer():

	@task
	def run():
		print('run')

	run()

consumer()