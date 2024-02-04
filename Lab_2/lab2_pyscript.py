#Question1: Multiply items together
part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

multiply = 1
for num in part1:
    multiply *= num
print('The answer to question 1 is: ', multiply)

#Question2: Add items together
part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]

sum = 0
for num in part2:
    sum += num
print('The answer to question 2 is: ', sum)

#Question3: Add only even items together
part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21] 

even_sum = 0
for num in part3:
 if num % 2 == 0:
    even_sum += num
print('The answer to question 3 is: ', even_sum)