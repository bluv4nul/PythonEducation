def findTarget(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i]+nums[j] == target:
                return i, j
    return 0, 0

nums = [2,7,11,15]
target = 9


i1, i2 = findTarget(nums, target)
if i1 == i2 == 0:
    print("Нет подходящих чисел")
else:
    print("i1 =", i1, " i2 =", i2)