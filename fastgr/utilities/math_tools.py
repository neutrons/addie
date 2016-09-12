def is_int(value):
    
    is_number = True
    try:
        int(value)
    except ValueError:
        is_number = False
        
    return is_number

def is_float(value):
    
    is_number = True
    try:
        float(value)
    except ValueError:
        is_number = False
        
    return is_number
    