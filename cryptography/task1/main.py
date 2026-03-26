import hashlib

input_string = input() 
    
md5_hex = hashlib.md5(input_string.encode('utf-8')).hexdigest()
sha256_hex = hashlib.sha256(input_string.encode('utf-8')).hexdigest()

print(md5_hex)
print(sha256_hex)
