import array 

def subdivide(array, k): 
    if len(array) % k != 0: 
        raise Exception("Array length must be divisible by k.") 
    partition_size = len(array) / k 
    return partition(array, partition_size) 

def partition(array, partition_size): 
    sub_arrays = []
    buffer = []
    for i in range(len(array)): 
        if i > 0 and i % partition_size == 0: 
            sub_arrays.append(buffer)
            buffer = []
        buffer.append(array[i])
    if len(buffer) > 0: 
        sub_arrays.append(buffer) 
    return sub_arrays 


def flatten(array):
    flattened = []
    for item in array: 
        flattened += item 
    return flattened

def encode_float_array_to_bytes(float_array): 
    items_b = array.array("f", float_array).tobytes() 
    return items_b 

def decode_bytes_to_float_array(bytes_): 
    data = array.array("f")
    data.frombytes(bytes_) 
    return data.tolist()