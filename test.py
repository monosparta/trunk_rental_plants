
soil_humi_percent = 100*(1 - 1555 / 4095)
print(F"{soil_humi_percent:4.2f}")

a = map(lambda x: 100*(1 - x / 4095), [x for x in range(4096)])

print([print(F"{i:4.2f}") for i in a])
