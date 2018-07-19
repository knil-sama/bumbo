# Purpose

Parse Hacker News search from a command line in python3

# Source 

https://gist.github.com/sfriquet/55b18848d6d58b8185bbada81c620c4a

# To run test

`docker-compose up --build test`

# To run api

`docker-compose up --build api`

# Warning

After the building stage the program will download the dataset and parse, this process take between **15 and 30 min**

# About assignment

I make use of pandas to load data from csv and into my datastructures, my goal was to aso use it as ref for the testing step
but the whole dependency can be replaced by a csv library of even just a open-> for -> split instead.

Also to insure that code can run anywhere I didn't store intermediate result of parsing that would be too big for github.

My goal was to begin with naive implementation in native type list and hashmap then move on to reimplement more complexe solution as skiplist and tree
but loading time was so high that I exceeded the deadline so I just focused on code readability and getting correct results.
