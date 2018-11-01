#############################################################################################################
#######################################LINEAR PROGRAMMING IN R###########################################################
#############################################################################################################

#########################################QUESTION################################################################
#A calculator company produces a scientific calculator and a graphing calculator. Long-term projections indicate an expected demand of at least 100 scientific and 80 graphing calculators #each day. Because of limitations on production capacity, no more than 200 scientific and 170 graphing calculators can be made daily. To satisfy a shipping contract, a total of at least 200 #calculators much be shipped each day.
##################################################################################################################
rm(list=ls(all=TRUE))
par(mfrow=c(1,1))

library(lpSolve)
##x: number of scientific calculators produced
#y: number of graphing calculators produced
#Objective
#max(-2x+5y)
#Constraint
#X should be produced more than 100 per day
#X should not be produced more than 200 per day
#Y should be produced more than 80 per day
#Y should not be produced more than 170 per day
obj=c(-2,5)
con=rbind(c(1,0), 
          c(1,0), 
          c(0,1), 
          c(0,1))


dir=c(">", "<", ">", "<")
rhs=c(100, 200, 80, 170)

res=lp("max", obj, con, dir, rhs,
       compute.sens=1)

#Analyzing the results

res$solution
## in order to maximize the profit one has to produce 100 scientific and 170 graphing calculator
res
# 650
