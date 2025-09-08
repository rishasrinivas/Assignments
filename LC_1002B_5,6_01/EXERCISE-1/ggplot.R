# Load required libraries
library(ggplot2)
library(dplyr)


data <- read.csv("C:\\Users\\DELL\\Downloads\\growth_rate_20220907.csv")


data_clean <- na.omit(data)

# --- 1. Bar Plot: Average Doubling Time for Selected Models ---
# This plot compares the average doubling time of different cell models.
doubling_times <- data_clean %>%
  group_by(model_name) %>%
  summarise(avg_doubling_time = mean(doubling_time_hours, na.rm = TRUE)) %>%
  arrange(desc(avg_doubling_time)) %>%
  head(10)

ggplot(doubling_times, aes(x = reorder(model_name, -avg_doubling_time), y = avg_doubling_time)) +
  geom_col(fill = "lightgreen") +
  geom_text(aes(label = round(avg_doubling_time, 2)), vjust = -0.5, size = 3) +
  labs(
    title = "Average Doubling Time of Top 10 Cell Models",
    x = "Cell Model Name",
    y = "Doubling Time (Hours)"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# --- 2. Scatter Plot: Seeding Density vs. Doubling Time ---
# This plot visualizes the relationship between the initial seeding density
ggplot(data_clean, aes(x = seeding_density, y = doubling_time_hours)) +
  geom_point(color = "darkorange", alpha = 0.7) +
  labs(
    title = "Seeding Density vs. Doubling Time",
    x = "Seeding Density",
    y = "Doubling Time (Hours)"
  ) +
  theme_minimal() +
  geom_smooth(method = "lm", se = FALSE, color = "dodgerblue") # Add a linear trend line

# --- 3. Line Plot: Doubling Time Over Ranked Replicates ---
data_ordered <- data_clean %>%
  arrange(seeding_density) %>%
  mutate(replicate_rank = row_number())

ggplot(data_ordered, aes(x = replicate_rank, y = doubling_time_hours)) +
  geom_line(color = "purple") +
  geom_point(color = "purple") +
  labs(
    title = "Doubling Time Trend Across Replicates (Ordered by Seeding Density)",
    x = "Replicate Rank",
    y = "Doubling Time (Hours)"
  ) +
  theme_minimal()
