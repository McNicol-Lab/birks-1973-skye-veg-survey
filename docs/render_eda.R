args <- commandArgs(trailingOnly = TRUE)
open_output <- !("--no-open" %in% args)

input_file <- "docs/skye_veg_eda.Rmd"
output_file <- "docs/skye_veg_eda.html"
required_pkgs <- c(
  "dplyr", "tidyr", "readr", "stringr", "forcats", "purrr", "tibble",
  "ggplot2", "ggrepel", "patchwork", "RColorBrewer", "scales",
  "vegan", "cluster", "knitr", "kableExtra", "here", "glue",
  "leaflet", "plotly", "DT", "htmltools", "rmarkdown", "indicspecies", "permute", "sf"
)

if (!file.exists(input_file)) {
  stop("Input file not found: ", input_file, call. = FALSE)
}

missing_pkgs <- required_pkgs[!vapply(required_pkgs, requireNamespace, logical(1), quietly = TRUE)]

if (length(missing_pkgs) > 0) {
  stop(
    paste0(
      "Missing R packages: ", paste(missing_pkgs, collapse = ", "),
      ". Run `Rscript docs/install_packages.R` first."
    ),
    call. = FALSE
  )
}

rendered_file <- rmarkdown::render(
  input = input_file,
  output_file = basename(output_file),
  output_dir = dirname(output_file),
  envir = new.env(parent = globalenv())
)

rendered_file <- normalizePath(rendered_file, winslash = "/", mustWork = TRUE)
message("Rendered: ", rendered_file)

if (open_output) {
  os_name <- Sys.info()[["sysname"]]
  open_cmd <- switch(
    os_name,
    "Darwin" = "open",
    "Linux" = "xdg-open",
    "Windows" = "cmd",
    ""
  )

  if (identical(open_cmd, "cmd")) {
    system2(open_cmd, c("/c", "start", "", shQuote(rendered_file)), wait = FALSE)
    message("Opened in default browser.")
  } else if (!identical(open_cmd, "")) {
    system2(open_cmd, shQuote(rendered_file), wait = FALSE)
    message("Opened in default browser.")
  } else {
    warning("Unsupported OS for automatic open: ", os_name, call. = FALSE)
  }
}
