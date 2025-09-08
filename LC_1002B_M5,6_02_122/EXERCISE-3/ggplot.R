library(tidyverse)

filepath <- "C:\\Users\\DELL\\Downloads\\heart_failure_clinical_records_dataset.csv"
if (!file.exists(filepath)) {
  stop("Error: The file 'heart_failure_clinical_records_dataset.csv' was not found.")
}

df <- read_csv(filepath)

# --- Line Plot: Average Ejection Fraction over Time ---
line_plot_data <- df %>%
  group_by(time) %>%
  summarise(avg_ejection_fraction = mean(ejection_fraction, na.rm = TRUE))

line_plot <- ggplot(line_plot_data, aes(x = time, y = avg_ejection_fraction)) +
  geom_line(color = "darkblue", size = 1.2) +
  geom_point(color = "darkblue", size = 2) +
  labs(
    title = "Average Ejection Fraction Over Follow-up Time",
    subtitle = "Trend shows average heart ejection rate across the study duration",
    x = "Follow-up Time (days)",
    y = "Average Ejection Fraction (%)"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5, color = "grey50"))

print(line_plot)

# --- Bar Plot: Death Events by Sex ---

df$sex_label <- factor(df$sex, levels = c(0, 1), labels = c("Female", "Male"))

bar_plot <- ggplot(df, aes(x = sex_label, fill = as.factor(DEATH_EVENT))) +
  geom_bar(position = "stack") +
  scale_fill_manual(values = c("No" = "lightgreen", "Yes" = "firebrick"),
                    labels = c("No Death Event", "Death Event")) +
  labs(
    title = "Number of Death Events by Sex",
    subtitle = "A count of fatal events broken down by gender",
    x = "Sex",
    y = "Count of Patients",
    fill = "Death Event"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5, color = "grey50"))

print(bar_plot)

# --- Scatter Plot: Serum Creatinine vs. Ejection Fraction ---

scatter_plot <- ggplot(df, aes(x = serum_creatinine, y = ejection_fraction, color = as.factor(DEATH_EVENT))) +
  geom_point(alpha = 0.7, size = 3) +
  labs(
    title = "Relationship Between Serum Creatinine and Ejection Fraction",
    subtitle = "Each point represents a patient; color indicates outcome",
    x = "Serum Creatinine (mg/dL)",
    y = "Ejection Fraction (%)",
    color = "Death Event"
  ) +
  scale_color_manual(values = c("0" = "darkgreen", "1" = "darkred"),
                     labels = c("No", "Yes")) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5, color = "grey50"))

print(scatter_plot)
