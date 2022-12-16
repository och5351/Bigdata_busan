### 함수 구성
def random_branch_path():
	from random import randint
	return 'cal_a_id' if randint(1, 2) == 1 else 'cal_m_id'

def calc_add(x, y, **kwargs):
	result = x + y
	print('x+y : ', result)
	kwargs['task_instance'].xcom_push(key='calc_result', value=result)

def calc_mul(x, y, **kwargs):
	result = x * y
	print('x*y : ', result)
	kwargs['task_instance'].xcom_push(key='calc_result', value=result)
	return 'calc mul'

def print_result(**kwargs):
	r = kwargs['task_instance'].xcom_pull(key='calc_result')
	print('message : ', r)
	print('*' * 100)
	print(kwargs)

def end_seq():
	print('end')


### operator로 dag task 구성
start = BashOperator(
	task_id = 'start',
	bash_command = 'echo "Start!"',
)

branch = BranchPythonOperator(
	task_id = 'branch',
	python_callable = random_branch_path,
)

calc_add = PythonOperator(
	task_id = 'cal_a_id',
	python_callable = calc_add,
	op_kwargs = {'x': 10, 'y': 4}
)

calc_mul = PythonOperator(
	task_id = 'cal_m_id',
	python_callable = calc_mul,
	op_kwargs = {'x': 10, 'y': 4}
)

msg = PythonOperator(
	task_id = 'msg',
	python_callable = print_result,
	trigger_rule = TriggerRule.NONE_FAILED
)

complete_py = PythonOperator(
	task_id = 'complete_py',
	depend_on_past = end_seq,
	trigger_rule = TriggerRule.NONE_FAILED
)

complete = BashOperator(
	task_id = 'complete_bash',
	depends_on_past = False,
	bash_command = 'echo "Complete~!"'
	trigger_rule = TriggerRule.NONE_FAILED
)

start >> branch >> calc_add >> msg >> complete_py >> complete
start >> branch >> calc_mul >> msg >> complete