""" 
    Point Loader
    --- 
    Loads and save a point from a .bin file.s
""" 
import os 
import math
import array
import src.backend.utils.helpers as helpers

class PointsLoader: 
    def load(
        file_path, 
        dims, 
        batch_size = 200000,
        on_load_points = None
    ):
        file = open(file_path, "rb")
        contents = file.read()
        file.close()
        file_size = os.path.getsize(file_path)
        sub_arrays = [] 
        sub_array_size = dims * 4 
        batch_size_bytes = sub_array_size * batch_size 
        vector_count = math.ceil(file_size / sub_array_size) 
        batch_size = min(batch_size, vector_count)
        count = 0
        for i in range(0, file_size, batch_size_bytes): 
            sub_array_bytes = contents[i:i + batch_size_bytes]
            sub_array_all = helpers.decode_bytes_to_float_array(sub_array_bytes)
            sub_array_chunks = helpers.subdivide(sub_array_all, batch_size) 
            sub_arrays += sub_array_chunks 
            if on_load_points: on_load_points(sub_array_chunks, count) 
            count += 1 
        return sub_arrays

    def save(
        file_path, 
        array, 
        dims,
        batch_size = 250000,
        on_save_points = None
    ): 
        # --- create container for buffer
        buffer = []
        
        # --- empty file 
        file = open(file_path, "wb")
        file.close()
        
        # --- append to file
        file = open(file_path, "ab")
        count = 0 
        for i in range(len(array)): 
            sub_array = array[i] 
            if i > 0 and i % batch_size == 0: 
                buffer_flat = helpers.flatten(buffer)
                bytes_ = helpers.encode_float_array_to_bytes(buffer_flat)
                file.write(bytes_) 
                if on_save_points: on_save_points(buffer, count)
                buffer = [] 
            buffer.append(sub_array)
            count += 1

        buffer_flat = helpers.flatten(buffer)
        bytes_ = helpers.encode_float_array_to_bytes(buffer_flat)
        file.write(bytes_)
        if on_save_points: on_save_points(buffer_count)

        file.close()

         