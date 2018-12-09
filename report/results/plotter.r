#!/usr/bin/env Rscript
dataset = read.csv("results.csv")

# Get distance error in metres
#distance_error = dataset$Distance - dataset$Predicted/100
#setEPS()
#postscript("distance-error.eps")
#plot(1:length(dataset$Distance),distance_error, ylab = "Error in metres", xlab = "#Frame")
#dev.off()

setEPS()
postscript("distance-comparason.eps")
plot(1:length(dataset$Distance),dataset$Predicted/100,ylab = "Distance", xlab = "#Frame", col = 2)
points(1:length(dataset$Distance),dataset$Distance)
dev.off()

# Get number of frames with more than one detection
table = table(dataset$Image)
frames = length(table[table > 1])

print(frames / length(table))

# Get detection time for each frame

#setEPS()
#postscript("detection-time.eps")
#plot(1:length(dataset$DetectionTime[-1]),dataset$DetectionTime[-1], ylim = c(0,1), ylab = "#Seconds", xlab = "#Frame")
#dev.off()
