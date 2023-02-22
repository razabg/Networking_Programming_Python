class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next



def main():



    head = ListNode()
    head = head.next
    if head:
        print("true")

    # a = ListNode(2)
    # b = ListNode(3)
    # c = ListNode(4)
    # d = ListNode(5)
    # head.next = a
    # a.next = b
    # b.next = c
    # c.next = d
    # temp = head
    # while temp.next is not None:
    #     print(temp.val,end="")
    #     print(" -> ",end="")
    #     temp = temp.next
    # print(temp.val)



if __name__ == '__main__':
    main()