import math

# 1️ Convert degree to radian
degree = 15
radian = degree * (math.pi / 180)

print("Degree:", degree)
print("Radian:", round(radian, 6))
print("-" * 40)


# 2️ Area of a trapezoid
height = 5
base1 = 5
base2 = 6

area_trapezoid = (base1 + base2) * height / 2

print("Height:", height)
print("Base1:", base1)
print("Base2:", base2)
print("Area of trapezoid:", area_trapezoid)
print("-" * 40)


# 3️ Area of regular polygon
n = 4
side = 25

area_polygon = (n * side**2) / (4 * math.tan(math.pi / n))

print("Number of sides:", n)
print("Side length:", side)
print("Area of polygon:", int(area_polygon))
print("-" * 40)


# 4️ Area of a parallelogram
base = 5
height_parallelogram = 6

area_parallelogram = base * height_parallelogram

print("Base:", base)
print("Height:", height_parallelogram)
print("Area of parallelogram:", float(area_parallelogram))