# Install necessary packages if not already installed
if (!require("caret")) install.packages("caret", dependencies = TRUE)
if (!require("pROC")) install.packages("pROC")
if (!require("randomForest")) install.packages("randomForest", dependencies = TRUE)

# Load the libraries
library(caret)
library(pROC)
library(randomForest)

# Load the data
validation_data <- read.csv("validation_data.csv")

# Assuming the CSV has columns named 'actual_labels' and 'model_predictions'
# Replace these with the actual column names in your CSV
actual_labels <- factor(validation_data$Actual_Label)
model_predictions <- factor(validation_data$Predicted_Label)

# Ensure levels are consistent for confusion matrix
levels(model_predictions) <- levels(actual_labels)

# Print levels to help diagnose the issue
print("Levels of actual_labels:")
print(levels(actual_labels))
print("Levels of model_predictions:")
print(levels(model_predictions))


# Perform statistical tests
# Confusion Matrix
confusionMatrix(model_predictions, actual_labels)

roc_obj <- roc(response = actual_labels, predictor = as.numeric(model_predictions))
plot(roc_obj)
auc(roc_obj)