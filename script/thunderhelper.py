# coding: utf-8
import base64
s = 'QUFlZDJrOi8vfGZpbGV8wsy8/S5BcnJvdy5TMDFFMDEuQ2hpX0VuZy5XRUItSFIuQUMzLjEwMjRYNTc2LngyNjQtWVllVHPIy8jL07DK0y5ta3Z8NTA2MTM1NTI3fDI0ZWEzZGY1OThmYWYxMGQ5YTdkNzA3Yzk4YTM4NDNhfGg9MnQzNmU0YmwyazVwejRneDYycTRiZ2lpdng2b2oyb3F8L1pa'

a = base64.b64encode(s)
print a
print type(a)
print type(s)

print base64.b64decode(s).decode("gbk").encode("utf-8")

s1 = 'QUFlZDJrOi8vfGZpbGV8wsy8'
print base64.b64decode(s1)
