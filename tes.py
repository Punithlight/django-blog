

# def duplicate(s):
#     for i in range(len(s)):
#         for j in range(i+1,len(s)):
#             if s[i]==s[j]:
#                 print("duplicate",s[i])
                
# duplicate([1,2,2,3,3,4])



# def palindrome(s):
#     i=0
#     j=len(s)-1
#     while i<j:
#         if s[i]!=s[j]:
#             return False
#         i=i+1
#         j=-1
#     return True

# print(palindrome("madam"))


def array():
    arr=[]
    while True:
        try:
            n=int(input("enetr the number for the array"))
            arr.append(n)
            
        except Exception as e:
            
        return arr
