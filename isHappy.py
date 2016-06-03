class Solution(object):
    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """
        nums = []
        while n != 1:
        	if n in nums:
        		return False
        	nums.append(n)
        	x = len(str(n))
        	m = 0
        	for i in range(0, x):
        		m = int(str(n)[i])**2 + m
        	n = m
        return True
