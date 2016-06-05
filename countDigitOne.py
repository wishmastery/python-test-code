class Solution(object):
    def countDigitOne(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n <= 0: return 0
        digit = len(str(n))
        if digit == 1: return 1
        first = int(str(n)[0])
        rest = int(str(n)[1:])
        if first != 1: return first*self.countDigitOne(10**(digit-1)-1) + 10**(digit-1) + self.countDigitOne(rest)
        else: return self.countDigitOne(10**(digit-1)-1) + self.countDigitOne(rest) + rest + 1
