from collections import Counter


class Solution:
    def isPalindrome(self, s: str) -> bool:
        a = s.replace(" ", "")
        a = a.lower()
        for i in a:
            if not i.isalnum():
                a = a.replace(i, "")

        if a[::-1] == a:
            return True
        else:
            return False


def main():
    sol = Solution()

    answer = sol.isPalindrome("0P")
    print(answer)
    answer = sol.isPalindrome(" ")
    print(answer)
    answer = sol.isPalindrome("A man, a plan, a canal: Panama")
    print(answer)



"""main"""
if __name__ == "__main__":
    main()
