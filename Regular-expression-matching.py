class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        # base case
        if p == '': return s == p
    	
    	if len(p) == 1: return s == p or (p == '.' and len(s) == 1)

    	# p1 != *
    	if p[1] != '*': 
    		return len(s) > 0 and (s[0] == p[0] or p[0] =='.') and self.isMatch(s[1:], p[1:])
    	
    	s2 = s

    	def concise(p):
    		n = len(p)
    		if n > 3:
    			if p[1] == '*' and p[3] == '*' and p[0] == p[2]:
    				return p[0:2] + concise(p[4:])
    			return p[0:2] + concise(p[2:])
    		return p


    	p = concise(p)

    	# p1 == *
    	while (len(s) > 0 and (s[0] == p[0] or p[0] == '.')): 
    		if self.isMatch(s[1:], p[2:]): return True
    		s = s[1:]

    	return self.isMatch(s2, p[2:])
