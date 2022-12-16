def func1(**context):
	# DB 접속 정보
    conn = pymysql.connect(host='/host/',
                           user='/user/',
                           password='/password/',
                           port = /port/,
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM DBNAME.DBTABLE;"
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    '''
    전처리 과정
    '''
    dct = df.to_dict()
    return dct  # 이 때 task1에서 xcom_push를 쓰지 않고 함수의 return을 이용해도 됨
    
def func2(**context):
	response = context['task_instance'].xcom_pull(task_ids = 'task1_id') #task_instance 대신 ti로 축약하여 써도 됨
	print(response['col1'])
	

task1 = PythonOperator(
    task_id = 'task1_id',
    python_callable = func1,
    provide_context = True,
    dag = init_dag
    )
	
task2 = PythonOperator(
    task_id = 'task2_id',
    python_callable = func2,
    provide_context = True,
    dag = init_dag
    )

task1 >> task2