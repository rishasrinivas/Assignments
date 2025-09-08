# Exercise 6 - R: Decision Tree on Heart Failure dataset

# Step 1: Load libraries
if(!require(rpart)) install.packages("rpart")
if(!require(rpart.plot)) install.packages("rpart.plot")
if(!require(caret)) install.packages("caret")

library(rpart)
library(rpart.plot)
library(caret)

# Step 2: Load dataset
heart_failure_data <- read.csv("heart_failure_clinical_records_dataset.csv")


# Step 3: Train/test split
set.seed(42)
# Assuming 'DEATH_EVENT' is the target variable
trainIndex <- createDataPartition(heart_failure_data$DEATH_EVENT, p=0.7, list=FALSE)
trainData <- heart_failure_data[trainIndex, ]
testData <- heart_failure_data[-trainIndex, ]

# Step 4: Train decision tree
# Assuming 'DEATH_EVENT' is the target variable and all other columns are features
tree_model <- rpart(DEATH_EVENT ~ ., data=trainData, method="class")

# Step 5: Predictions
pred <- predict(tree_model, testData, type="class")

# Step 6: Evaluation
# The reference levels in confusionMatrix should match the levels in the test data
confusionMatrix(pred, factor(testData$DEATH_EVENT))


# Step 7: Visualization
rpart.plot(tree_model, main="Decision Tree - Heart Failure Dataset")
