def numStructer(bai, shi, ge):
	return bai*100 + shi*10 + ge


nums = [1,2,4,5,8,9]
cha_max = 0
cha_min = 999
cha_175 = []

for bai1 in nums:
	nums_temp = nums[:]
	nums_temp.remove(bai1)
	for shi1 in nums_temp:
		nums_temp.remove(shi1)
		for ge1 in nums_temp:
			nums_temp.remove(ge1)
			for bai2 in nums_temp:
				nums_temp.remove(bai2)
				for shi2 in nums_temp:
					nums_temp.remove(shi2)
					ge2 = nums_temp[0]
					a = numStructer(bai1, shi1, ge1)
					b = numStructer(bai2, shi2, ge2)
					print(a,b)
					cha = abs(a - b)
					if cha>cha_max:
						cha_max = cha
					if cha<cha_min:
						cha_min = cha
					if cha == 175:
						cha_175.append(a,b)


print(cha_175, cha_min, cha_max)