# Lab 02 Activity: Palindrome check karta hai.
# Word ko reverse karke original se compare karta hai.
# capitalize() ki wajah se first-letter case ka farq ignore hota hai.

def ispalindrome(word):
    temp=word[::-1]
    if temp.capitalize()==word.capitalize():
        return True
    else:
        return False
print(ispalindrome("deed"))
