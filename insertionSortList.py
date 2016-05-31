
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def insertionSortList(self, head):
        ans = head
        if ans == None: return ans
        ans = [ListNode(head.val)]
        while(head.next != None):
            ans.append(ListNode(head.next.val))
            head = head.next
        ans.sort(key = lambda ListNode : ListNode.val)
        i = 0
        while i + 1 < len(ans): 
            ans[i].next = ans[i + 1]
            i += 1
        return ans[0]


# ln1 -> ln2 -> ln3
# 5 -> 1 -> 3
ln1 = ListNode(2)
ln2 = ListNode(7)
ln3 = ListNode(3)
ln4 = ListNode(0)
ln1.next = ln2
ln2.next = ln3
ln3.next = ln4

s = Solution()
h = s.insertionSortList(ln1)
print(h.val, h.next.val, h.next.next.val, h.next.next.next.val)
