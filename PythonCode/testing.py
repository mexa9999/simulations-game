from ctypes import *

awesome = cdll.LoadLibrary("./GoCode/awesome.so")
awesome.Add.argtypes = [c_int, c_int]
print("awesome.Add(12,99) = %d" % awesome.Add(12,99))

awesome.Cosine.argtypes = [c_double]
awesome.Cosine.restype = c_double 
cos = awesome.Cosine(1)
print("awesome.Cosine(1) = %f" % cos)

class GoSlice(Structure):
    _fields_ = [("data", POINTER(c_void_p)),
                ("len", c_longlong), ("cap", c_longlong)]
    
    def to_list(self):
        return self.data[:self.len]

nums = GoSlice((c_void_p * 5)(74, 4, 122, 9, 12), 5, 5)
awesome.Sort.argtypes = [GoSlice]
awesome.Sort.restype = None
awesome.Sort(nums)

class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]
c_char
awesome.Log.argtypes = [GoString]
msg = GoString(b"Hello Python!", 13)
awesome.Log(msg)