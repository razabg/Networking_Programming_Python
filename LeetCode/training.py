from typing import Optional



#Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:


tergerg









def main():

    head = ListNode(1)
    a = ListNode(2)
    b = ListNode(4)
    head.next = a
    a.next = b

    head2 = ListNode(1)
    c = ListNode(3)
    d = ListNode(4)
    head2.next = c
    c.next = d

    temp = head
    while temp.next is not None:
        print(temp.val,end="")
        print(" -> ",end="")
        temp = temp.next
    print(temp.val)

    temp = head2
    while temp.next is not None:
        print(temp.val, end="")
        print(" -> ", end="")
        temp = temp.next
    print(temp.val)

    sol = Solution()
    res = sol.mergeTwoLists(head,head2)
    temp = res
    while temp.next is not None:
        print(temp.val,end="")
        print(" -> ",end="")
        temp = temp.next
    print(temp.val)

if __name__ == '__main__':
    main()
