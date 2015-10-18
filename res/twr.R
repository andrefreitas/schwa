TIME_RANGE = 0.5

twr_modified = function(ti){
  1 / (1 + exp(-(12) * ti + 2 + ((1-TIME_RANGE) * 10)))
}
twr = function(ti){
  1 / (1 + exp(-12 * ti + 12))
}
plot(twr_modified, 0, 1,  xlab="ti")
#plot (twr, 0, 1, add=TRUE)

title(main = "TR=0.5")
