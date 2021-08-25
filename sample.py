obj = [{
    "name": "IMG_20200213_110950_M030.jpg",
    "lines": 1,
    "mean": 145.50840579710146,
    "median": 178,
},{
    "name": "IMG_20200213_110950_M030.jpg",
    "lines": 2,
    "mean": 146.2330754352031,
    "median": 178,
},{
    "name": "IMG_20200213_110938_M025.jpg",
    "lines": 1,
    "mean": 152.66072300928187,
    "median": 187,
},
{
    "name": "IMG_20200213_110938_M025.jpg",
    "lines": 2,
    "mean": 155.85752808988764,
    "median": 187,
},
{
    "name": "IMG_20200213_110938_M025.jpg",
    "lines": 3,
    "mean": 152.12388250319285,
    "median": 187,
}
]

for i in obj:
    print(i["name"], i["lines"], i["mean"], i["median"],)
