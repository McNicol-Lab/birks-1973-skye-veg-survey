# Run this once to install the packages required by docs/skye_veg_eda.Rmd.
pkgs <- c(
  "dplyr", "tidyr", "readr", "stringr", "forcats", "purrr", "tibble",
  "ggplot2", "ggrepel", "patchwork", "RColorBrewer", "scales",
  "vegan", "cluster", "knitr", "kableExtra", "here", "glue",
  "leaflet", "plotly", "DT", "htmltools", "rmarkdown", "indicspecies", "permute", "sf"
)

missing <- pkgs[!pkgs %in% installed.packages()[, "Package"]]

if (length(missing) > 0) {
  message("Installing: ", paste(missing, collapse = ", "))
  install.packages(missing, repos = "https://cloud.r-project.org")
} else {
  message("All packages already installed.")
}
