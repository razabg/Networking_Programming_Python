from typing import Optional



#Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr = head
        prev = None
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        return prev






def main():

    head = ListNode(1)
    a = ListNode(2)
    b = ListNode(3)
    c = ListNode(4)
    d = ListNode(5)
    head.next = a
    a.next = b
    b.next = c
    c.next = d
    temp = head
    while temp.next is not None:
        print(temp.val,end="")
        print(" -> ",end="")
        temp = temp.next
    print(temp.val)

    sol = Solution()
    res = sol.reverseList(head)
    temp = res
    while temp.next is not None:
        print(temp.val,end="")
        print(" -> ",end="")
        temp = temp.next
    print(temp.val)

if __name__ == '__main__':
    main()
