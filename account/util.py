import random
import time



def generate_matric_number():
    year=time.strftime("%Y")
    rand_digits=random.randint(200000,900000)
    return f"PU{year}{rand_digits}"