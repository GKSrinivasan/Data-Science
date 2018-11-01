library(lpSolve)

#Consider a small manufacturer making two products P1 and P2. Two resources R1 and R2
#are required to make these products. Each unit of product P1 requires 1 unit of R1 and 3
#units of R2. Each unit of product P2 requires 1 unit of R1 and 2 units of R2. The
#manufacturer has 5 units of R1 and 12 of R2 available
#The manufacturer also make a profit of
#Rs 6 per unit of product P1 sold and
#Rs 5 per unit of product P2 sold


# Problem Formulation
# Decision variables : Represent the solution for the problem.
#   X1: Number of units of P1 produced.
#   X2: Number of units of P2 produced.
# Objective Function
#   Z : 6 X1 + 5 X2 Maximize
# Constrains 
#   1 X1 + 1 X2 <= 5
#   3 X1 + 2 X2 <= 12
# Non negativity restriction 
#   X1 >= 0
#   X2 >= 0

# A Linear Programming problem has
# - a linear objective function
# - linear constraints and
# - the non negativity constraints on all the decision variables. 

obj = c(6, 5)
con = rbind(c(1, 1), 
            c(3, 2),
            c(1, 0), 
            c(0, 1))
dir = c("<=", "<=", ">=", ">=")
rhs = c(5, 12, 0, 0)
res = lp("max", obj, con, dir, rhs, int.vec = c(1,2) )
#Analyzing the results
res$solution
res

#Dual program
obj = c(5, 12)
con = rbind(c(1, 3), 
            c(1, 2),
            c(1, 0), 
            c(0, 1))
dir = c(">=", ">=", ">=", ">=")
rhs = c(6, 5, 0, 0)
res = lp("min", obj, con, dir, rhs)
res$solution
res



#Problem Satement 1
#Blue Ridge Hot Tubs manufactures and sells two models of hot tubs: the Aqua-Spa and the
#Hydro-Lux. Howie Jones, the owner and manager of the company, needs to decide how
#many of each type of hot tub to produce during his next production cycle.
#Howie buys prefabricated fiberglass hot tub shells from a local supplier and adds the
#pump and tubing to the shells to create his hot tubs. (This supplier has the capacity to
#deliver as many hot tub shells as Howie needs.)
#Howie installs the same type of pump into both hot tubs. He will have only 200 pumps
#available during his next production cycle. From a manufacturing standpoint, the main
#difference between the two models of hot tubs is the amount of tubing and labour required.
#Each Aqua-Spa requires 9 hours of labour and 12 feet of tubing. Each Hydro-Lux requires 6
#hours of labour and 16 feet of tubing.
#Howie expects to have 1,566 production labour hours and 2,880 feet of tubing available
#during the next production cycle. Howie earns a profit of $350 on each Aqua-Spa he sells
#and $300 on each Hydro-Lux he sells. He is confident that he can sell all the hot tubs he
#produces. The question is, how many Aqua-Spas and Hydro-Luxes should Howie produce if
#he wants to maximize his profits during the next production cycle. How many Aqua-Spas
#and Hydro-Luxes should be produced? http://www.chegg.com/homework-help/questions-
#and-answers/om300-hw6-3-pages-due-class-time-friday-10-10-2014-fall-2014-problem-1-
#40-points-instructi-q5941967
obj=c(350,300)
con=rbind(c(1,1), c(9,6), c(12, 16),
          c(1,0), c(0, 1))
dir=c("<=", "<=", "<=", ">=", ">=")
rhs=c(200, 1566, 2880, 0, 0)
res=lp("max", obj, con, dir, rhs, int.vec = c(1,2) )
#Analyzing the results
res$solution
res



#Dual program
obj=c(200,1566, 2888)
con=rbind(c(1,9,12), c(1,6,16),
          c(1,0,0), c(0, 1,0), c(0,0, 1) )
dir=c(">=", ">=", ">=", ">=",">=")
rhs=c(350,300,0,0,0)
res=lp("min", obj, con, dir, rhs)
res$solution
res


#Problem statement 2
#  A furniture maker has 6 units of wood and 28 hours of free time. Two models were sold well in
#the past. Model 1 requires 2 units of wood and 7 hours and model 2 requires 1 unit of wood and
#8 hours of time. Prices are Rs. 200 and 150 each. How many of each should he make to maximize
#the revenues?
f.obj = c(200, 150)
f.con = matrix (c(2, 1, 7, 8, 1, 0, 0, 1), nrow=4, byrow=TRUE)
f.dir = c("<=", "<=", ">=", ">=")
f.rhs = c(6,28,0,0)
#Linear Programming
res=lp("max", f.obj, f.con, f.dir, f.rhs)
res$solution
res

#Integer Programming

lp ("max", f.obj, f.con, f.dir, f.rhs, int.vec=1:2)
lp ("max", f.obj, f.con, f.dir, f.rhs, int.vec=1:2)$solution


#Problem statement 3
#Consider the following product mix example (Hadley, 1962). A shop that has three machines, A, B,
#and C, turns out four different products. Each product must be processed on each of the three
#machines (for example, lathes, drills, and milling machines). The following table shows the number
#of hours required by each product on each machine:
#  Product
#Machine 1 2 3 4
#A 1.5 1 2.4 1
#B 1 5 1 3.5
#C 1.5 3 3.5 1
#The weekly time available on each of the machines is 2,000, 8,000, and 5,000 hours, respectively.
#The products contribute 5.24, 7.30, 8.34, and 4.18 to profit, respectively. What mixture of products
#can be manufactured to maximize profit?
f.obj = c(5.24, 7.30, 8.34, 4.18)
f.con = matrix (c(1.5, 1, 2.4, 1, 1, 5, 1, 3.5, 1.5, 3, 3.5,1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1), nrow=7, byrow=TRUE)
f.dir = c("<=", "<=", "<=", ">=", ">=",">=",">=")
f.rhs = c(2000,8000,5000,0,0,0,0)
#Linear Programming
lp ("max", f.obj, f.con, f.dir, f.rhs)
lp ("max", f.obj, f.con, f.dir, f.rhs )$solution


#Problem 5
#Problem Statement 5: Product mix using Solver.
#There are 4 panel types that have to be produce using the given resources. The resources are Glue,
#Pressing, Pine chips and Oak chips. However, Glue is available only 5800 quarts, Pressing is 730
#hours, Pine chips are 29200 pounds and Oak chips are about 60500 pounds. The profits of producing
#various panel types Tahoe is $450, Pacific is $ 1150, Savannah is $800 and Aspen is $400. Using the
#available resources, find the amount of pallets that can be produced in order to maximize the profits
#of producing various panel types.
obj=c(450, 1150,800, 400)
con=rbind(c(50,50,100,50), c(5,15,10,5), c(500,400,300,200),c(500,750,250,500),
          c(1,0,0,0), c(0, 1,0,0), c(0, 1,0,0),c(0, 0,1,0))
dir=c("<=", "<=", "<=", "<=", ">=",">=", ">=",">=")
rhs=c(5800, 730, 292200,32500,0,0,0,0)
res=lp("max", obj, con, dir, rhs)
#Analyzing the results
res$solution
res

#Problem 6
#Problem Statement 6: Assignment problem
#There are 4 jobs and 4 workers. Given is the matrix of costs when a job is assigned to a worker. What
#is the best allocation of jobs to workers such that the cost is minimized?
#Build the cost matrix
cost_mat=matrix(c(1,2,3,4,2,4,6,8,3,6,9,12,4,8,12,16),nrow = 4, byrow = T)

#Using the function: lp.assign(cost.mat ,direction) 
a=lp.assign(cost.mat=cost_mat,direction = "min")
#Analyzing the results
a$solution
a



#Problem 7:
#You have $12,000 to invest, and three different funds from which to choose. The municipal
#bond fund has a 7% return, the local bank's CDs have an 8% return, and the high-risk account
#has an expected (hoped-for) 12% return. To minimize risk, you decide not to invest any more
#than $2,000 in the high-risk account. For tax reasons, you need to invest at least three times
#as much in the municipal bonds as in the bank CDs. Assuming the year-end yields are as
#expected, what are the optimal investment amounts.
library(lpSolve)
obj=c(-0.05,-0.04)
con=rbind(c(1,0),c(0,1),c(1,1),c(1,1),c(1/3,-1))
dir=c(">=",">=",">=","<=",">=")
rhs=c(0,0,10,12,0)
res=lp("max",obj,con,dir,rhs)
res$solution
res
#-0.475

#Y=1.44 - 0.05x - 0.04y
#Y=1.44-0.475=0.965


#Problem 8:
#Transportation Problem
#Linear Programming: Transportation Problem
#1. Formulate the way in which the products can be transported from origin to destination at the
#minimum cost for the below matrix.
#FROM\TO
#DC1
#DC2
#DC3
#SUPPLY
#BOSTON 5 6 4 300
#TORONTO 6 3 7 500
#200 300 250
#DEMAND
#Also, write down the objective functions and constraints for this.
rm(list=ls(all=TRUE)) 

#Load the package
library(lpSolve)

#Define the cost matrix
cost_mat=matrix(c(5,6,4,6,3,7),nrow = 2,byrow = T)

#Set the directions
row_s=c("<=","<=")

#Supply available from Plants
row_rhs=c(300,500)

#Direction of Demand Centres
col_s=c("=","=","=")

#Demands of Demand Centres
col_rhs=c(200,300,250)

#Analyse the result 
res=lp.transport(cost.mat = cost_mat,direction ="min" ,row.signs =row_s ,row.rhs = row_rhs,col.signs = col_s,col.rhs = col_rhs)
res$solution
res
