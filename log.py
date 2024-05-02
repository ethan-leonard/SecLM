import time

def log(task_id):
    global start_time
    
    if 'start_time' not in globals():
        start_time = time.time()
    else:
        end_time = time.time()
        elapsed_time = end_time - start_time
        log_entry = f"{task_id}: {elapsed_time} seconds\n"
        with open("log.txt", "a") as log_file:
            log_file.write(log_entry)
        start_time = time.time()