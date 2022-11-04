library(tidyverse)
library(here)
library(arrow)
library(plotly)
here::i_am('src/RI_distribution/preprocess_distribution_metrics.R')
data <- read_csv(here("data/processed/distribution_metrics.csv"))

preprocess_data <- data %>%
    mutate(project = ifelse(str_detect(target, "sepsis"), "sepsis", "igra"), .after=target) %>%
    mutate(cell_type = ifelse(str_detect(target, 'CD4'), 'CD4', 'CD8'), .after=project) %>%
    mutate(time = str_extract(target, "[0-9]{8}\\.[0-9]{6}\\.[0-9]{3}"), .after=cell_type) %>%
    mutate(patient = map_chr(target, ~str_split(.x, '/')[[1]][7]), .after =project) %>%
    select(-target) %>% 
    mutate(time = lubridate::as_datetime(time))

min_time_table <- preprocess_data %>% 
    group_by(project, patient) %>%
    summarize(min_time = min(time))

final_data <- preprocess_data %>% 
    left_join(min_time_table, by = c("project", "patient")) %>%
    mutate(diff_min =difftime(time, min_time, units='mins'), .before = time) %>%
    mutate(diff_min_int = floor(diff_min), .before = time)

fig_median_point <- ggplot(final_data, aes(x = diff_min, y = value_50, color = patient)) +
    geom_point() +
    facet_wrap(project ~ cell_type, scale = 'free') + 
    theme_bw() +
    theme(legend.position = "none") +
    labs(x = "Time (minutes)", y = "RI median", color = "Patient")
fig_median_point

fig_mean_point <- ggplot(final_data, aes(x = diff_min, y = value_mean, color = patient)) +
    geom_point() +
    facet_wrap(project ~ cell_type, scale = 'free') + 
    theme_bw() +
    theme(legend.position = "none") +
    labs(x = "Time (minutes)", y = "RI mean", color = "Patient")
ggplotly(fig_mean_point)

fig_min_point <- ggplot(final_data, aes(x = diff_min, y = value_min, color = patient)) +
    geom_point() +
    facet_wrap(project ~ cell_type, scale = 'free') + 
    theme_bw() +
    theme(legend.position = "none") +
    labs(x = "Time (minutes)", y = "RI mean", color = "Patient")
fig_min_point

fig_max_point <- ggplot(final_data, aes(x = diff_min, y = value_100, color = patient)) +
    geom_point() +
    facet_wrap(project ~ cell_type, scale = 'free') + 
    theme_bw() +
    theme(legend.position = "none") +
    labs(x = "Time (minutes)", y = "RI mean", color = "Patient")
fig_max_point

fig_smooth <- final_data %>% 
    select(project, cell_type, diff_min, value_0 = value_min, value_25, value_50, value_75, value_100) %>%
    pivot_longer(cols = starts_with("value"), names_to = "percentile", values_to = "value") %>%
    mutate(percentile = factor(percentile, levels = c("value_0", "value_25", "value_50", "value_75", "value_100"))) %>%
    ggplot(aes(x = diff_min, y = value, color = percentile)) +
    geom_smooth() + 
    facet_wrap(project ~ cell_type, scale = 'free') + 
    theme_bw() + 
    scale_colour_manual(labels = c('0', '25', '50', '75', '100'), values = c('#99d8c9','#66c2a4','#238b45','#238b45','#005824')) + 
    theme(legend.position = "bottom") +
    labs(x = "Time (minutes)", y = "RI", color = "Percentile")
fig_smooth

ggsave("figure/RI_median_point_distribution.pdf", fig_median_point, width = 8, height = 6)
ggsave("figure/RI_mean_point_distribution.pdf", fig_mean_point, width = 8, height = 6)
ggsave("figure/RI_smooth_distribution.pdf", fig_smooth, width = 8, height = 6)

